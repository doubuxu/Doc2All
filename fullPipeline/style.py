from openai import OpenAI
from jinja2 import Template
from pathlib import Path
from dotenv import load_dotenv
import argparse
import base64
import os
import re
import tempfile
from shutil import which


INTERACTION_PROMPT_PATH = Path("./prompts/webInteraction.txt")
STYLE_PROMPT_PATH = Path("./prompts/webStyle.txt")
STYLE_API_KEY_ENV = "API_KEY"
STYLE_BASE_URL_ENV = "BASE_URL"
STYLE_MODEL_ENV = "STYLE_MODEL"
STYLE_VLM_MODEL_ENV = "STYLE_VLM_MODEL"
STYLE_BROWSER_PATH_ENV = "STYLE_BROWSER_PATH"


load_dotenv()


def load_prompt(html: str, prompt_path: Path) -> str:
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


def encode_image_as_data_url(image_path: Path) -> str:
    image_bytes = image_path.read_bytes()
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def get_client() -> OpenAI:
    api = os.getenv(STYLE_API_KEY_ENV)
    url = os.getenv(STYLE_BASE_URL_ENV)
    return OpenAI(api_key=api, base_url=url)


def get_generation_model_name() -> str:
    return os.getenv(STYLE_MODEL_ENV, "your-style-model-placeholder")


def get_vlm_model_name() -> str:
    return os.getenv(STYLE_VLM_MODEL_ENV, get_generation_model_name())


def get_browser_executable_path():
    browser_from_env = os.getenv(STYLE_BROWSER_PATH_ENV)
    if browser_from_env:
        return browser_from_env

    candidates = [
        Path.home() / ".cache/ms-playwright/chromium-1208/chrome-linux64/chrome",
        Path.home() / ".cache/ms-playwright/chromium-1161/chrome-linux/chrome",
        Path.home() / ".cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell",
        Path.home() / ".cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/chrome-headless-shell",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    for command_name in ["chromium", "chromium-browser", "google-chrome"]:
        command_path = which(command_name)
        if command_path:
            return command_path
    return None


def render_html_preview(html_path: Path, preview_path: Path, viewport_width: int = 1440, viewport_height: int = 2000) -> Path:
    from playwright.sync_api import sync_playwright

    preview_path.parent.mkdir(parents=True, exist_ok=True)
    executable_path = get_browser_executable_path()

    with sync_playwright() as playwright:
        launch_kwargs = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],
        }
        if executable_path:
            launch_kwargs["executable_path"] = executable_path

        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=1,
        )
        page.goto(html_path.resolve().as_uri(), wait_until="load")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(preview_path), full_page=True)
        browser.close()

    return preview_path


def generate_interactive_html(html: str, prompt_path: Path = INTERACTION_PROMPT_PATH) -> str:
    client = get_client()
    model_name = get_generation_model_name()
    prompt = load_prompt(html, prompt_path=prompt_path)

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        temperature=0,
        extra_body={"enable_thinking": False},
    )
    return extract_html_from_response(response.choices[0].message.content)


def generate_styled_html(html: str, preview_image_path: Path, prompt_path: Path = STYLE_PROMPT_PATH) -> str:
    client = get_client()
    model_name = get_vlm_model_name()
    image_data_url = encode_image_as_data_url(preview_image_path)
    prompt = load_prompt(html, prompt_path=prompt_path)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data_url},
                    },
                ],
            }
        ],
        stream=False,
        temperature=0,
        extra_body={"enable_thinking": False},
    )
    return extract_html_from_response(response.choices[0].message.content)


def style_html(
    html: str,
    interaction_prompt_path: Path = INTERACTION_PROMPT_PATH,
    style_prompt_path: Path = STYLE_PROMPT_PATH,
    preview_image_path: Path | None = None,
) -> tuple[str, Path]:
    interactive_html = generate_interactive_html(html, prompt_path=interaction_prompt_path)

    if preview_image_path is None:
        with tempfile.TemporaryDirectory(prefix="style_preview_") as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_html_path = temp_dir_path / "interactive.html"
            temp_preview_path = temp_dir_path / "interactive_preview.png"
            save_html(interactive_html, temp_html_path)
            render_html_preview(temp_html_path, temp_preview_path)
            styled_html = generate_styled_html(interactive_html, temp_preview_path, prompt_path=style_prompt_path)
            return styled_html, temp_preview_path

    with tempfile.TemporaryDirectory(prefix="style_preview_") as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_html_path = temp_dir_path / "interactive.html"
        save_html(interactive_html, temp_html_path)
        render_html_preview(temp_html_path, preview_image_path)
        styled_html = generate_styled_html(interactive_html, preview_image_path, prompt_path=style_prompt_path)
        return styled_html, preview_image_path


def build_styled_output_path(input_html_path: Path) -> Path:
    return input_html_path.with_name(f"{input_html_path.stem}_style{input_html_path.suffix}")


def build_preview_output_path(input_html_path: Path) -> Path:
    return input_html_path.with_name(f"{input_html_path.stem}_preview.png")


def main():
    parser = argparse.ArgumentParser(description="Enhance an existing HTML file in two stages: interaction first, then visual styling.")
    parser.add_argument("html_path", help="Path to the input HTML file")
    args = parser.parse_args()

    input_html_path = Path(args.html_path).resolve()
    html = load_html(input_html_path)

    preview_path = build_preview_output_path(input_html_path)
    styled_html, _ = style_html(html, preview_image_path=preview_path)
    output_html_path = build_styled_output_path(input_html_path)
    save_html(styled_html, output_html_path)


if __name__ == "__main__":
    main()
