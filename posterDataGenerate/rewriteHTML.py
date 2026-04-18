import argparse
import os
import re
from pathlib import Path

import dotenv
from openai import OpenAI

from planJson3 import parse_html_to_content_plan
from ImageInfo import enrich_content_plan2
dotenv.load_dotenv()

_CLIENT: OpenAI | None = None
_MODEL_NAME: str | None = None


def save_html(path: str | Path, html: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def _get_client() -> tuple[OpenAI, str]:
    global _CLIENT, _MODEL_NAME

    if _CLIENT is None:
        api_key = os.getenv("ALI_API", "")
        base_url = os.getenv("ALI_URL", "")
        _CLIENT = OpenAI(api_key=api_key, base_url=base_url)

    if _MODEL_NAME is None:
        _MODEL_NAME = (
            os.getenv("HTML_REWRITE_MODEL")
            or os.getenv("VISUAL_GENERATION_MODEL")
            or os.getenv("VISUAL_MODEL")
            or ""
        )

    return _CLIENT, _MODEL_NAME


def build_html_rewrite_prompt(_: str) -> str:
    return """
# 角色
你是一个专业的 HTML 语义重构工程师。你的任务是：对已有的学术海报 HTML 文件进行**纯语义层面的重写**，使其完全符合一套严格的 JSON 解析脚本提取标准。

# 核心原则（最高优先级）
1. **绝对禁止改变视觉排版**：不要添加、删除任何 CSS 类（如 Tailwind 类）、style 属性、布局 div。你的工作仅仅是**替换标签名、移动标签位置、添加/修改特定的 data-* 属性**。
2. **文本内容零损失**：所有文字、标点、数学符号必须原样保留，绝对不能意译、缩写或删减。

# 语义重写规则（必须严格执行）

请按照以下对照表，将输入 HTML 中的旧写法，逐个替换为新写法：

## 1. 顶层容器规范
- 【规则】全篇只能有 `<header>` 和 `<section>` 两种章节内容容器。
- 【重写】如果发现有 `<div class="abstract">`、`<div class="footer">`、`<div class="references">` 等，必须将外层标签改为 `<section id="section_n" data-type="section">`，并为里面的标题加上 `<h2>`。

## 2. Metadata 区域重写
- 【旧写法】标题、作者、机构的语义标签不规范。
- 【新写法】必须全部包裹进 `<header data-type="metadata">` 中：
  - 标题必须是 `<h1>标题</h1>`
  - 作者必须是 `<div data-type="authors">作者1, 作者2</div>`
  - 机构必须是 `<div data-type="organizations">机构1, 机构2</div>`
  - GitHub 链接必须是完整的 `<a href="https://github.com/...">文本</a>`

## 3. 图片与公式的属性重写（重点）
- 【旧写法】`<img src="./fig1.png">` 或 `<img class="figure" src="...">`
- 【新写法】必须在 `<img>` 标签本身上添加 `data-fig-id` 和 `data-type`，以及有意义的 `alt` 描述：
  - 普通图：`<img src="./figure_1.jpg" data-fig-id="figure_1" data-type="figure" alt="详细描述这张图的内容">`
  - 表格图：`<img src="./table_1.jpg" data-fig-id="table_1" data-type="table" alt="详细描述这个表格的数据对比内容">`
  - 公式图：`<img src="./eq1.jpg" data-fig-id="equation_1" data-type="figure" alt="描述这个公式的数学含义">` （注意：公式的 data-fig-id 必须以 `equation` 开头）
- 【注意】`data-fig-id` 的值必须与 `src` 中的文件名主体保持逻辑一致。

## 4. Caption（图注）的重写
- 【旧写法 A】图注直接跟在图片后面：`<img ...> <p>图1：这是说明</p>`
- 【新写法 A】必须用 `<figure>` 包裹，图注放入 `<figcaption>`：
  <figure>
  <img src="cat1.jpg" data-fig-id="figure_1" data-type="figure" alt="猫在睡觉">
  <figcaption>图1：小猫的一天日常</figcaption>
</figure>

## 特殊章节
- 【旧写法】References、Footer 等特殊章节没有统一规范，可能是 `<div class="references">` 或 `<footer>` 等。
- 【新写法】必须写成合法的 section，例如 `<section id="section_5" data-type="section">`，并且章节标题必须使用 `<h2>`。  

## 5. 超链接的重写
- 【旧写法】GitHub 链接可能只是纯文本，或者没有使用 `<a>` 标签。
- 【新写法】必须使用 `<a href="完整URL">文本</a>` 标签，并且 `href` 属性必须包含完整的 URL。    

## 返回要求
- 只输出完整 HTML。
- 以 `<!DOCTYPE html>` 开头。
- 不要输出 Markdown 代码块。
- 不要输出任何解释。
"""


def extract_html_from_response(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""

    fenced_patterns = [
        r"```html\s*(.*?)\s*```",
        r"```\s*(<!DOCTYPE html.*?</html>)\s*```",
        r"```\s*(<html.*?</html>)\s*```",
    ]
    for pattern in fenced_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    html_match = re.search(r"<!DOCTYPE html.*", text, re.DOTALL | re.IGNORECASE)
    if html_match:
        return html_match.group(0).strip()

    html_match = re.search(r"<html.*?</html>", text, re.DOTALL | re.IGNORECASE)
    if html_match:
        return html_match.group(0).strip()

    return text


def rewrite_html_with_llm(html_code: str, temperature: float = 0) -> str:
    client, model_name = _get_client()
    prompt_text = build_html_rewrite_prompt(html_code)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {"type": "text", "text": "INPUT_HTML:"},
                {"type": "text", "text": html_code},
            ],
        }
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    response_text = response.choices[0].message.content or ""
    rewritten_html = extract_html_from_response(response_text)
    if not rewritten_html.strip():
        raise ValueError("LLM returned empty HTML content.")
    return rewritten_html


def rewrite_html_file(html_path: str | Path, output_path: str | Path | None = None) -> str:
    html_path = Path(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    rewritten_html = rewrite_html_with_llm(html_code)

    if output_path is not None:
        save_html(output_path, rewritten_html)

    return rewritten_html


def batch_rewrite_poster_html(input_dir: str | Path) -> list[dict[str, str]]:
    input_dir = Path(input_dir)
    results: list[dict[str, str]] = []

    for subdir in sorted(p for p in input_dir.iterdir() if p.is_dir()):
        poster_html_path = subdir / "poster.html"
        if not poster_html_path.exists():
            continue

        poster_original_path = subdir / "poster_original.html"

        with open(poster_html_path, "r", encoding="utf-8") as f:
            original_html = f.read()

        rewritten_html = rewrite_html_with_llm(original_html)

        if not poster_original_path.exists():
            poster_html_path.rename(poster_original_path)

        save_html(poster_html_path, rewritten_html)
        json_path = parse_html_to_content_plan(str(poster_html_path), str(subdir))
        enrich_content_plan2(json_path=json_path)
        results.append(
            {
                "subdir": str(subdir),
                "original_html": str(poster_original_path),
                "rewritten_html": str(poster_html_path),
                "json_path": str(json_path),
            }
        )

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-path", type=str, help="Single HTML file to rewrite.")
    parser.add_argument(
        "--input-dir",
        type=str,
        help="Batch mode: iterate subfolders and rewrite each poster.html.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="Output path for single file mode.",
    )
    args = parser.parse_args()

    if args.html_path:
        rewritten_html = rewrite_html_file(args.html_path, args.output_path)
        print(f"Rewritten HTML characters: {len(rewritten_html)}")
        return

    if args.input_dir:
        results = batch_rewrite_poster_html(args.input_dir)
        print(f"Processed folders: {len(results)}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
