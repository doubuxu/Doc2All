from openai import OpenAI
from jinja2 import Template
from pathlib import Path
from dotenv import load_dotenv
import argparse
import os
import re


# 默认使用 web 风格化 prompt
STYLE_PROMPT_PATH = Path("./prompts/webStyle.txt")
STYLE_API_KEY_ENV = "API_KEY"
STYLE_BASE_URL_ENV = "BASE_URL"
STYLE_MODEL_ENV = "STYLE_MODEL"


load_dotenv()


def load_style_prompt(html: str, prompt_path: Path = STYLE_PROMPT_PATH) -> str:
    prompt_template = Template(prompt_path.read_text(encoding="utf-8"))
    return prompt_template.render(html=html)


def extract_html_from_response(content: str) -> str:
    raw = content.strip()
    fenced_match = re.search(r"(?s)^```(?:html)?\s*\n(.*?)\n```$", raw)
    if fenced_match:
        return fenced_match.group(1).strip()
    return raw


def load_html(html_path: Path) -> str:
    return html_path.read_text(encoding="utf-8")


def save_html(html: str, save_path: Path) -> None:
    save_path.write_text(html, encoding="utf-8")


def style_html(html: str, prompt_path: Path = STYLE_PROMPT_PATH) -> str:
    api = os.getenv(STYLE_API_KEY_ENV)
    url = os.getenv(STYLE_BASE_URL_ENV)
    model_name = os.getenv(STYLE_MODEL_ENV, "your-style-model-placeholder")

    client = OpenAI(
        api_key=api,
        base_url=url
    )

    prompt = load_style_prompt(html, prompt_path=prompt_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        temperature=0,
        extra_body={"enable_thinking": False}
    )
    styled_html = extract_html_from_response(response.choices[0].message.content)
    return styled_html


def build_styled_output_path(input_html_path: Path) -> Path:
    return input_html_path.with_name(f"{input_html_path.stem}_style{input_html_path.suffix}")


def main():
    parser = argparse.ArgumentParser(description="Style an existing HTML file with LLM.")
    parser.add_argument("html_path", help="Path to the input HTML file")
    args = parser.parse_args()

    input_html_path = Path(args.html_path).resolve()
    html = load_html(input_html_path)
    styled_html = style_html(html)
    output_html_path = build_styled_output_path(input_html_path)
    save_html(styled_html, output_html_path)


if __name__ == "__main__":
    main()
