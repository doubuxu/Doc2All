import base64
import json
import mimetypes
import os
import re
from pathlib import Path
from typing import Any
import dotenv

from openai import OpenAI

JsonDict = dict[str, Any]

_CLIENT: OpenAI | None = None
_MODEL_NAME: str | None = None
dotenv.load_dotenv()

def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_html(path: str | Path, html: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def extract_json_from_markdown(text: str | JsonDict | list[Any]) -> Any:
    if not isinstance(text, str):
        return text

    patterns = [
        r"```json\s*(.*?)\s*```",
        r"```\s*(.*?)\s*```",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1))

    return json.loads(text.strip())


def _get_client() -> tuple[OpenAI, str]:
    global _CLIENT, _MODEL_NAME

    if _CLIENT is None:
        api_key = os.getenv("API_KEY", "")
        base_url = os.getenv("BASE_URL", "")
        _CLIENT = OpenAI(api_key=api_key, base_url=base_url)

    if _MODEL_NAME is None:
        _MODEL_NAME = os.getenv("VISUAL_GENERATION_MODEL", "")

    return _CLIENT, _MODEL_NAME


def _encode_image_base64(image_path: str | Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _infer_image_mime_type(image_path: str | Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(image_path))
    return mime_type or "image/jpeg"


def _call_vlm_with_blocks(
    *,
    image_path: str | Path,
    text_blocks: list[str],
    temperature: float = 0,
) -> str:
    client, resolved_model_name = _get_client()

    user_content: list[JsonDict] = []
    for block in text_blocks:
        user_content.append({"type": "text", "text": block})

    user_content.append(
        {
            "type": "image_url",
            "image_url": {
                "url": (
                    f"data:{_infer_image_mime_type(image_path)};"
                    f"base64,{_encode_image_base64(image_path)}"
                )
            },
        }
    )

    messages: list[JsonDict] = [{"role": "user", "content": user_content}]

    response = client.chat.completions.create(
        model=resolved_model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def load_content_list_input(content_list_path: str | Path) -> list[Any]:
    return load_json(Path(content_list_path).resolve())


def resolve_content_list_path(image_path: str | Path, mineru_path: str | Path) -> Path:
    poster_name = Path(image_path).stem
    return Path(mineru_path) / poster_name / f"{poster_name}_content_list.json"


def build_layout_tree_prompt(_: JsonDict) -> str:
    return """
Role: 你是一位资深文档排版专家，擅长将复杂的学术海报（非结构化图像）转化为逻辑清晰的布局树（Layout Tree）。你的目标是为后续的响应式 HTML/CSS 生成提供核心结构。
Input:
    海报原图：用于感知视觉对齐、颜色块和隐性边界。
    MinerU JSON 数据：包含原子元素（text, image, table）的内容及精确坐标 bbox: [xmin, ymin, xmax, ymax]。
Task:请分析图像和 BBox 数据，构建一个 Layout Tree (JSON)。容器化：将语义相关的原子元素聚合为 panel。
    布局推导：识别海报的网格系统（如 3 栏布局）。
    处理异常：识别跨列（col-span）或跨行（row-span）的 Panel。
    判断标准：若 Panel 宽度明显超过单列宽度，标记为跨列。
    相对坐标：不使用绝对像素，使用 width_weight (0-1) 和 grid_area。
💡 参考样例 (Reference Example)User Input (MinerU snippet):[{"id": "t1", "text": "DGPs & Tests", "text_level": 1, "bbox": [28, 548, 117, 568]}, ...]
    Your Expected Output (Layout Tree):
    JSON{
  "poster_name": "[Re] Graph Edit Networks",
  "global_config": {
    "total_columns": 3,
    "theme": "academic_red_accent"
  },
  "layout_tree": [
    {
      "role": "header",
      "grid_area": { "row": 1, "col": 1, "col_span": 3 },
      "elements": ["header_0", "header_1", "header_2"]
    },
    {
      "role": "main_grid",
      "children": [
        {
          "id": "panel_intro",
          "title": "Reproduced: Paaβen et. al.",
          "grid_area": { "row": 1, "col": 1 },
          "width_weight": 0.33,
          "content": ["text_1", "fig_1", "text_3"]
        },
        {
          "id": "panel_spanning_dgps",
          "title": "DGPs & Tests",
          "note": "Detected as spanning across column 1 and 2 based on visual width",
          "grid_area": { "row": 2, "col": 1, "col_span": 2 },
          "style": { "background": "light-red-bar" },
          "content": ["text_5", "fig_2", "fig_3", "fig_4"]
        },
        {
          "id": "panel_results",
          "title": "Improving the experimental setup",
          "grid_area": { "row": 1, "col": 3, "row_span": 2 },
          "width_weight": 0.33,
          "content": ["text_20", "table_2", "list_1"]
        }
      ]
    }
  ]
}
🛠 推理逻辑指南 (Logical Guidelines for VLM):
    如何确定列数：观察海报中垂直空白间隙（Gutters）的数量。
    如何聚合 Panel：以 text_level: 1 的元素作为起始锚点，直到遇到下一个 text_level: 1 或明显的物理分割线。
    如何处理跨列：计算单列期望宽度 $W_{col} \approx PosterWidth / TotalColumns$。如果 $PanelWidth > 1.2 \times W_{col}$，则设 col_span: 2 或更多。
    输出要求：仅输出符合格式的 JSON，不要解释。
"""


def build_html_generation_prompt(_: JsonDict) -> str:
    return """
你是一位顶级的全栈工程师，专精于将复杂的学术海报逆向工程为结构化、语义化的响应式 HTML。你的目标是确保生成的代码在视觉布局、阅读顺序、图文对应关系和 HTML 结构风格上与现有 htmlGenerate3 的输出规范保持一致，并且后续能够稳定提取为学术 PlanJSON。

### 输入数据
1. 海报原图：这是布局、字体层级、并列关系和整体视觉结构的唯一最终依据。
2. layout tree JSON：这是第一阶段已经推断好的层级布局结果，描述 panel、header、main grid、section、跨列关系、容器关系和阅读顺序。你必须以它作为结构和布局实现的核心依据。
3. MinerU content_list JSON：这份数据只能用于确认最终 HTML 中必须出现哪些元素、文本内容、图片/表格/公式等对象以及它们的原始字段。你**不能**使用 content_list 的 bbox、顺序或相对坐标来分析布局，也**不能**用它替代 layout tree 做布局推断。

### Chain-of-Thought 分析步骤
#### 步骤 1：全局结构确认
- 首先观察海报原图，确认页眉、正文主体、页脚/参考文献区等全局区域。
- 然后读取 layout tree，确认整体网格结构、每个 panel 的层级归属、阅读顺序、跨列/跨行关系以及主次分区。
- 如果海报图片与 layout tree 在局部细节上有轻微冲突，以“海报原图 + layout tree”共同决定布局；其中结构和分组优先服从 layout tree，视觉比例和字体层级优先服从海报原图。

#### 步骤 2：元素清单与内容保全
- 读取 content_list，仅用于确定最终 HTML 中应当保留的元素集合。
- 你必须保留所有原始文本内容、图片元素、表格元素、公式元素、列表元素及其图注/表注。
- 如果 content_list 中出现图片、表格、公式、标题、正文、列表等对象，最终 HTML 中必须有对应元素承载这些内容。
- 严禁使用 content_list 的 bbox、绝对位置、扫描顺序来决定布局；这些信息在第二阶段仅可忽略。
- 不能遗漏原始海报中的任何元素，即使它们在 content_list 中没有明确标记，也必须根据海报图片进行还原。

##### 子图、表格和独立公式的处理
- 对于最终的html，其中包括的图片和表格通过content_list中的path确定，例如content_list中的路径是"../posterData/mineru_output_with_eq/[Re] Graph Edit Networks_poster/visuals/images/fig_7.jpg"，则最终html中对应的图片元素应该是<img src="./fig_7.jpg" >，并且这个图片元素必须保留原始文本内容（如果有的话）和图注（如果有的话）。
- 你需要根据输入的content_list中的图片和表格与海报图片进行对应，确定生成的html中各个子图和表格在哪个panel中，并且在html中正确地使用<figure>和<figcaption>标签来包裹图片和表格元素，以及它们的图注/表注。
- 你需要确保生成的html中的图片和表格元素具有正确的语义信息字段semantic-info
- 对于content_list中标记为equation的元素，你需要在html中使用其图片路径来渲染内容而不是直接使用latex代码，图片路径的使用方式同上文描述的图片元素的处理方式。例如content_list中的公式图片路径是"../posterData/mineru_output_with_eq/Flexible Attention-Based Multi-Policy Fusion for Efficient Deep Reinforcement Learning_poster/visuals/equations/equations_5.jpg"，在html中应该渲染为<img src="./equations_5.jpg" >，并且这个图片元素必须保留原始文本内容（如果有的话）和图注（如果有的话），同时具有正确的语义信息字段semantic-info来标识这是一个公式元素。

##### content_list中不存在的元素
- 对于海报中存在，但content_list中不存在的元素，你首先需要判断这个元素的类别
- 如果是文本元素，你需要严格按照海报图片中的文本内容来还原，并且在html中使用<p>标签来承载这个文本内容
- 如果是图片元素，你需要在html中使用<img>标签来承载这个图片元素，并且src属性指向这个图片的虚拟相对路径，例如"./logo.jpg",虚拟相对路径的文件名与这个子图的语义保持一致，你需要估算图片的大小，实际渲染一个矩形占位符来表示。

#### 字体与间距的确定和识别
- 字体大小和间距大小是影响布局的重要因素，我的输入信息中不包含具体的字体大小和间距数值，你需要根据输入的海报图片来估计和推断这些信息。
- 在推断这些信息的时候，你需要结合海报中的已知信息，例如图片的大小，不同层级字体之间的相对大小关系，不同元素之间的相对位置关系等，来综合判断和推断出合理的字体大小和间距大小。
- 你需要确保推断出的字体大小和间距大小能够帮助你更好地还原海报的视觉布局和层级关系，并且能够在后续的html生成中得到体现。

#### 海报风格属性的省略
- 你的任务是还原海报的布局结构和阅读顺序，而不是复刻海报的视觉风格细节。因此，你不需要在html中复刻海报的背景色、边框、装饰性图形等纯视觉元素。
- 针对字体或背景的颜色，你直接使用默认的白底黑字，不必关注色彩信息的还原。
- 针对边框、分割线、装饰性图形等元素，如果它们在海报中没有承载文本或图表内容，也不影响海报的布局设计，则将这些属性或元素省略。


#### 步骤 3：结构化 HTML 设计
- HTML风格：从视觉海报生成一个独立、可运行、语义化的单文件响应式 HTML。
- 整体语义树必须呈现 `[Header(Metadata)] -> [Main(Sections)] -> [Footer(References)]` 的层级。
- 每个学术章节必须用 `<section id="section_n">` 包裹，其中 `n` 为从 1 开始递增的整数。
- 章节标题使用 `<h2>`，必要时子标题用 `<h3>`，正文使用 `<p>`，列表使用 `<ul>/<li>`。
- 图片和表格优先使用 `<figure>` 包裹，图注/表注使用 `<figcaption>`。
- 数学公式需要在 `<head>` 中配置 MathJax，以支持 LaTeX 渲染。
- 线性源码顺序要符合人类阅读顺序，而不是 OCR 或 content_list 的原始顺序。

#### 步骤 4：响应式布局实现
- 禁止使用 `position: absolute` 复刻布局。
- 必须基于 layout tree 中的层级关系，使用 `grid`、`flex`、嵌套容器和合理的 `gap/padding/margin` 构建布局。
- 大屏固定： 使用一个 max-width 容器，在桌面端缩放减小时，布局保持居中且结构稳定不变，布局与原图保持一致。
- 移动端响应： 使用 CSS Grid 或 Flexbox。当缩放放大（视口宽度小于某个值）时，触发响应式断点，将多列布局转变为单列堆叠布局。
- 需要通过海报原图估计字体层级：主标题、章节标题、子标题、正文、图注、参考文献应有清晰的字号差异，但无需追求像素级一致。
- 重点还原布局、阅读结构和 typography，不必复刻背景色、边框和纯装饰细节。
- 底部强制对齐：如果海报布局是规则的多栏，你必须识别出每一列（Column）中的最后一个节点，并为其添加 margin-top: auto; 或 flex-grow: 1; 的样式，以确保所有列的底部在视觉上严格对齐。

### 关键硬约束
1. layout tree 是第二阶段布局推理的核心依据。
2. content_list 只能用于“元素枚举、文本保全、图表对象确认、data-fig-id 对应”，不能用于布局分析。
3. 所有图片 `<img>` 都必须保留原始标识信息；如果能确定对应图号，必须写入 `data-fig-id`。
4. 在关键容器上使用 `data-type`，取值范围仅限：`metadata`、`abstract`、`section`、`figure`、`table`、`reference`。
5. 不能删除、改写、压缩或概括原始文本内容。
6. 输出必须是独立的单文件 HTML，通过 CDN 引入 Tailwind。
7. 最终输出只允许是 HTML 代码本身，不允许输出解释文字、注释性前言、Markdown 代码块或思维过程。

### MathJax 配置要求
在 `<head>` 中必须包含以下脚本：
<script>
  window.MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

### 输出要求
- 只输出完整 HTML。
- 以 `<!DOCTYPE html>` 开头。
- 不要输出 Markdown 代码块。
- 不要输出任何解释。
"""


def generate_layout_tree(
    *,
    content_list_path: str | Path,
    image_path: str | Path,
) -> JsonDict:
    image_path = Path(image_path).resolve()
    content_list_path = Path(content_list_path).resolve()
    content_list = load_content_list_input(content_list_path)
    prepared_input = {
        "poster_name": image_path.stem,
        "image_path": str(image_path),
        "content_list_path": str(content_list_path),
        "content_list_dir": str(content_list_path.parent),
        "content_list": content_list,
    }
    prompt_text = build_layout_tree_prompt(prepared_input)

    response_text = _call_vlm_with_blocks(
        image_path=prepared_input["image_path"],
        text_blocks=[
            prompt_text,
            "INPUT_CONTENT_LIST_JSON:",
            json.dumps(prepared_input["content_list"], ensure_ascii=False, indent=2),
        ],
        temperature=0,
    )
    return extract_json_from_markdown(response_text)


def generate_html_from_layout_tree(
    *,
    layout_tree: JsonDict,
    content_list_path: str | Path,
    image_path: str | Path,
) -> str:
    content_list = load_content_list_input(content_list_path)
    prepared_input = {
        "image_path": str(Path(image_path).resolve()),
        "layout_tree": layout_tree,
        "content_list_path": str(Path(content_list_path).resolve()),
        "content_list": content_list,
    }
    prompt_text = build_html_generation_prompt(prepared_input)

    return _call_vlm_with_blocks(
        image_path=prepared_input["image_path"],
        text_blocks=[
            prompt_text,
            "INPUT_LAYOUT_TREE_JSON:",
            json.dumps(layout_tree, ensure_ascii=False, indent=2),
            "INPUT_CONTENT_LIST_JSON:",
            json.dumps(content_list, ensure_ascii=False, indent=2),
        ],
        temperature=0,
    )

def responsiveHTMLGenerate(
    *,
    image_path: str | Path,
    mineru_path: str | Path,
) -> str:
    content_list_path = resolve_content_list_path(image_path, mineru_path)
    layout_tree = generate_layout_tree(
        content_list_path=content_list_path,
        image_path=image_path,
    )

    html_code = generate_html_from_layout_tree(
        layout_tree=layout_tree,
        content_list_path=content_list_path,
        image_path=image_path,
    )

    return html_code


def batchImagesGenerate(
    *,
    image_dir: str | Path,
    mineru_path: str | Path,
    output_dir: str | Path,
) -> None:
    image_dir = Path(image_dir)
    mineru_path = Path(mineru_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

    for image_path in image_dir.iterdir():
        if image_path.suffix.lower() not in image_extensions:
            continue

        poster_name = image_path.stem
        content_list_path = resolve_content_list_path(image_path, mineru_path)
        if not content_list_path.exists():
            print(f"[SKIP] missing content list: {content_list_path}")
            continue

        poster_output_dir = output_dir / poster_name
        poster_output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[Processing] {poster_name}")
        try:
            html = responsiveHTMLGenerate(
                image_path=image_path,
                mineru_path=mineru_path,
            )
            save_html(poster_output_dir / f"{poster_name}.html", html)
            print(f"  [OK] html length={len(html)}")
        except Exception as exc:
            print(f"  [FAIL] {poster_name}: {exc}")


if __name__ == "__main__":
    example_image_path = "../small_batch_data/Flexible Attention-Based Multi-Policy Fusion for Efficient Deep Reinforcement Learning_poster.jpg"
    example_html_path = "./layout_tree_test.html"
    example_mineru_path = "../posterData/batchData1/mineru_output_with_eq"

    if Path(example_image_path).exists():
        html = responsiveHTMLGenerate(
            image_path=example_image_path,
            mineru_path=example_mineru_path,
        )
        save_html(example_html_path, html)
        print(f"Generated HTML characters: {len(html)}")
