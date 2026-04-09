from openai import OpenAI
from jinja2 import Template
from pathlib import Path
from dotenv import load_dotenv
import argparse
import base64
import os
import re
import tempfile
from typing import Tuple
from shutil import which


BASE_DIR = Path(__file__).resolve().parent
INTERACTION_PROMPT_PATH = BASE_DIR / "prompts" / "webInteraction.txt"
STYLE_PROMPT_PATH = BASE_DIR / "prompts" / "webStyle.txt"
STYLE_API_KEY_ENV = "API_KEY"
STYLE_BASE_URL_ENV = "BASE_URL"
STYLE_MODEL_ENV = "STYLE_MODEL"
STYLE_VLM_MODEL_ENV = "STYLE_VLM_MODEL"
STYLE_BROWSER_PATH_ENV = "STYLE_BROWSER_PATH"

INTERACTION_TABLE_GUIDELINES = """
表格交互专项要求：
- 必须识别页面中所有 `.doc2all-table-wrapper` 内的原生 `<table>`，把它们视为需要重点增强的学术数据表。
- 不得修改表格中的任何文本、数字、公式、引用编号、行列顺序、表头层级、rowspan、colspan。
- 允许增加不会改变表格信息结构的属性、按钮、工具栏、包装容器、`data-*` 标记、`aria-*` 属性和脚本。
- 每个表格都要补充一个轻量工具栏，工具栏至少包含：
  1. `Copy table` 按钮：点击后复制该表格的纯文本制表符版本到剪贴板；成功后同一个按钮短暂显示 `Copied!` 再恢复。
  2. `Search` 输入框：仅过滤当前表格的行；匹配时保留表头；搜索为空时恢复全部行。
  3. 排序能力：点击列头可以对当前表格按该列升序/降序切换；优先按数值排序，无法解析为数值时按文本排序；排序必须尽量保持表头结构不变。
- 首行首列固定：
  - 对每个数据表实现 `sticky` 首行和首列。
  - 具体做法：表头单元格使用 `position: sticky; top: 0; z-index` 分层；第一列单元格使用 `position: sticky; left: 0; z-index` 分层。
  - 首行首列交叉的左上角单元格必须有最高层级并有不透明背景，避免滚动时穿透。
- 横向和纵向滚动都必须在表格局部容器内完成，不得让整个页面因为表格交互而抖动。
- 查找、排序、复制脚本必须是渐进增强：当页面有多个表格时，每个表格独立工作，互不干扰。
- 表格交互代码必须尽量原生、轻量、自包含；不要引入大型表格库。
- 要考虑学术网页场景的可用性：
  - 对过宽表格保留横向滚动。
  - 工具栏在窄屏下允许换行，但不能遮挡表格内容。
  - 给搜索框、排序状态、复制按钮增加合理的 `aria-label` 或文本提示。
- 如果某个表格结构过于复杂，无法完美支持排序，也不要破坏原表；应优先保证表格可读与滚动可用，再提供尽可能稳定的排序行为。
"""

STYLE_TABLE_GUIDELINES = """
表格视觉专项要求：
- 必须识别页面中所有 `.doc2all-table-wrapper` 内的 `<table>`，把它们作为学术网页的数据表来统一美化。
- 不得修改表格中的任何文本、数字、公式、引用编号、行列顺序、rowspan、colspan；只能补充样式和少量不改变结构的属性。
- 表格整体视觉方向：
  - 学术网页风格
  - 克制、清晰、编辑型
  - 信息密度高但不压迫
- 每个表格都应呈现为卡片式数据模块：
  - 外层 wrapper 与页面卡片体系一致
  - 表格工具栏、表头、表体、表注之间层次清楚
  - 不要把表格做成产品后台或商业 BI 仪表盘风格
- 必须明确优化以下项目，并给出可落地做法：
  1. 奇偶行交错色彩：使用非常轻的 zebra striping，提高长表可读性，但不能过饱和。
  2. 背景色彩：表头、固定首列、hover 行、排序激活列应有低对比但清晰的背景区分。
  3. 卡片式：为表格容器增加边框、圆角、柔和阴影、内外留白，并与正文块保持节奏统一。
- 推荐补充的真实学术网页细节：
  - 表头字重略强于正文，必要时可加细边框或下边线。
  - 数字列可使用更利于比较的对齐方式和字距，但不要改内容。
  - 首行首列在固定状态下必须有不透明背景，避免与滚动内容重叠。
  - 搜索框、复制按钮、排序状态要有统一、低干扰的视觉样式。
  - 表格 caption 或紧邻的说明文字要与表格形成一组，但不要改写 caption 文本。
  - 深浅主题下都要保证表格边界、斑马纹、hover、sticky 区域可区分。
- 对 `.doc2all-table-wrapper` 里的裸表格，尽量补足以下视觉层级：
  - `<table>` 的整体宽度、字体、分隔线和单元格间距
  - `<thead>` 的背景、字重、粘性阴影或分隔
  - `<tbody>` 的行分隔、hover 态、zebra striping
  - `<th>` / `<td>` 的 padding、边界、垂直对齐
- 不要改变字号大小这一硬约束，但可以通过颜色、字重、边框、背景和阴影提升层级。
"""


load_dotenv()


def load_prompt(html: str, prompt_path: Path) -> str:
    prompt_template = Template(prompt_path.read_text(encoding="utf-8"))
    prompt_name = prompt_path.name.lower()
    table_guidelines = ""
    if "interaction" in prompt_name:
        table_guidelines = INTERACTION_TABLE_GUIDELINES
    elif "style" in prompt_name:
        table_guidelines = STYLE_TABLE_GUIDELINES
    return prompt_template.render(html=html, table_guidelines=table_guidelines)


def extract_html_from_response(content: str) -> str:
    raw = content.strip()
    fenced_match = re.search(r"(?s)^```(?:html)?\s*\n(.*?)\n```$", raw)
    if fenced_match:
        return fenced_match.group(1).strip()
    return raw


def is_complete_html_document(html: str) -> Tuple[bool, str]:
    required_markers = ["<!DOCTYPE html>", "<html", "</html>", "<head", "</head>", "<body", "</body>"]
    for marker in required_markers:
        if marker not in html:
            return False, f"missing required marker: {marker}"

    if html.count("<style") != html.count("</style>"):
        return False, "unbalanced <style> tags"
    if html.count("<script") != html.count("</script>"):
        return False, "unbalanced <script> tags"

    if html.rstrip()[-7:].lower() != "</html>":
        return False, "document does not end with </html>"

    return True, "ok"


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
    retry_suffix = (
        "\n\n补充硬约束：\n"
        "- 输出必须是完整 HTML 文档，必须包含 `<head>...</head>`、`<body>...</body>`、`</html>`。\n"
        "- 严禁输出半截 `<style>` 或半截 `<script>`。\n"
        "- 不要为了增强交互而生成超长重复 CSS；优先写少量、语义化、作用域明确的选择器。\n"
    )

    current_prompt = prompt
    last_html = ""
    last_error = "no response"
    for attempt in range(2):
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": current_prompt}],
            stream=False,
            temperature=0,
            extra_body={"enable_thinking": False},
        )
        candidate_html = extract_html_from_response(response.choices[0].message.content)
        is_valid, reason = is_complete_html_document(candidate_html)
        if is_valid:
            return candidate_html
        last_html = candidate_html
        last_error = reason
        current_prompt = prompt + retry_suffix + f"\n上一次输出失败原因：{reason}\n请重新输出完整 HTML。"

    raise ValueError(f"Interactive HTML generation returned incomplete HTML: {last_error}\nPartial output:\n{last_html[:1000]}")


def generate_styled_html(html: str, preview_image_path: Path, prompt_path: Path = STYLE_PROMPT_PATH) -> str:
    client = get_client()
    model_name = get_vlm_model_name()
    image_data_url = encode_image_as_data_url(preview_image_path)
    prompt = load_prompt(html, prompt_path=prompt_path)
    retry_suffix = (
        "\n\n补充硬约束：\n"
        "- 输出必须是完整 HTML 文档，必须包含 `<head>...</head>`、`<body>...</body>`、`</html>`。\n"
        "- 严禁输出半截 `<style>` 或半截 `<script>`。\n"
        "- 表格样式必须用少量高层级、语义化选择器实现，例如 `.doc2all-table-wrapper table`、`thead th`、`tbody tr:nth-child(even)`。\n"
        "- 严禁枚举式重写几十上百个 Tailwind 工具类，例如连续生成大量 `.text-*`、`.bg-*`、`.px-*`、`.py-*` 规则。\n"
        "- 不要输出冗长重复 CSS；优先保持样式精简。\n"
    )

    current_prompt = prompt
    last_html = ""
    last_error = "no response"
    for attempt in range(2):
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": current_prompt},
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
        candidate_html = extract_html_from_response(response.choices[0].message.content)
        is_valid, reason = is_complete_html_document(candidate_html)
        if is_valid:
            return candidate_html
        last_html = candidate_html
        last_error = reason
        current_prompt = prompt + retry_suffix + f"\n上一次输出失败原因：{reason}\n请重新输出完整 HTML。"

    raise ValueError(f"Styled HTML generation returned incomplete HTML: {last_error}\nPartial output:\n{last_html[:1000]}")


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
