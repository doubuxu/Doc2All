import base64
from pathlib import Path
import shutil
import sys
import os
import mimetypes
from openai import OpenAI

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 或者获取当前工作目录
# current_dir = os.getcwd()

# 插入到路径列表的最前面（优先搜索）
sys.path.insert(0, current_dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import load_json,save_json
from utils.htmlTools import save_html
# 或者添加到末尾
# sys.path.append(current_dir)

from HandcodeHtmlGenerate import generate_poster_html,get_image_size
import dotenv
import json
from PIL import Image
import io
dotenv.load_dotenv()
"""
poster->mineru->根据结果手动编码html->VLM->最终HTML
"""

def image_encode(img_path):
        with open(img_path, "rb") as f:
            img_data = f.read()
        encoded_str = base64.b64encode(img_data).decode("utf-8")
        return encoded_str

def get_verified_base64_image(img_path):
    # 使用 Pillow 打开图片
    with Image.open(img_path) as img:
        # 强制转换模式为 RGB (防止 PNG 的透明通道在转 JPG 时报错)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # 将图片重新保存到内存中的字节流，格式严格指定为 JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        
        # 获取重新编码后的 Base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def responsiveHTMLGenerate(image_path,mineru_path):
    """
    提供image的完整路径，
    mineru的输出路径是最外层的路径，根据image_path获取文件名，进而获取content_list和middle_json
    """
    poster_name = Path(image_path).stem
    poster_w,poster_h=get_image_size(image_path)
    content_list_path = Path(mineru_path)/f"{poster_name}"/f"{poster_name}_content_list.json"
    middle_json_path = Path(mineru_path)/f"{poster_name}"/f"{poster_name}_middle.json"
    content_list = load_json(content_list_path)
    middle_json = load_json(middle_json_path)

    absolute_html = generate_poster_html(content_list,middle_json,poster_w,poster_h)



    api=os.getenv("API_KEY")
    url=os.getenv("BASE_URL")
    model_name=os.getenv("VISUAL_MODEL","qwen3-max")
    client=OpenAI(
        api_key=api,
        base_url=url
    )
    #mime_type, _ = mimetypes.guess_type(img_path)

# 2. 如果识别失败，给一个默认值
    #if not mime_type:
    #    mime_type = "image/jpeg"
    prompt_content = f"""
你是一位顶级的全栈工程师，专精于将复杂的视觉海报逆向工程为“结构化、语义化”的响应式 HTML。你的目标是确保生成的代码不仅在视觉上完美还原，且能通过脚本轻松提取为学术 PlanJSON 格式。

### 输入数据
1. **海报原图**：作为布局和语义逻辑的最终判定标准。
2. **绝对定位 HTML 源码**：提供原始内容、图片 ID (data-fig-id) 及像素级坐标参考。

### 任务要求：遵循以下 Chain-of-Thought (CoT) 逻辑分析
#### 步骤 1：空间与并列关系扫描
- **全局分栏识别**：通过图片识别海报的大框架（如：三栏布局、页眉页脚）。
- **横向并列判定**：检查 HTML 源码中元素的 Y 轴重叠情况。如果两个块垂直区间重叠且 left 不同，判定为“横向并列”。
- **语义分块**：根据原图标题，将海报划分为 Introduction, Methodology 等逻辑章节。

#### 步骤 2：结构化 HTML 约束 (面向 PlanJSON 提取)
- **容器化 (Wrapping)**：必须使用 `<section id="section_n">` 包裹每个独立章节。
- **层级分明**：章节标题统一使用 `<h2>`，子标题使用 `<h3>`，正文使用 `<p>`。
- **数据锚点注入**：
    - 必须为每个 `<img>` 或其容器保留原始的 `data-fig-id`。
    - 在关键容器上标注 `data-type` (如 "abstract", "reference", "figure")。
- **数学公式渲染**：必须在 <head> 中配置 MathJax 以解析 LaTeX 公式。请务必包含以下脚本：
    <script>
      window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }} }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
- **线性阅读顺序**：确保源码中的元素顺序符合人类逻辑，而非 OCR 识别的随机顺序。

#### 步骤 3：响应式布局实现 (Tailwind CSS)
- 移除所有 `position: absolute`。
- 使用 `grid` 或 `flex` 替代坐标。在桌面端 (lg) 强制保留横向并排结构，在移动端 (md 以下) 自动垂直堆叠。

### 输出约束
- 仅关注 **Layout** (布局、间距、对齐)。使用 Tailwind 的 gap, padding, margin。
- 忽略颜色、背景、边框等装饰性样式。
- **严禁删除任何原始文本内容。**

### ⚠️ 面向 PlanJSON 提取的终极硬约束：
1. **语义树结构**：HTML 必须呈现 [Header(Metadata)] -> [Main(Sections)] -> [Footer(References)] 的层级。
2. **章节唯一性**：每个学术章节必须包裹在 <section id="section_n"> 中，其中 n 是从 1 开始的递增整数。
3. **图文关联**：所有的图片 (<img>) 必须带有原始的 data-fig-id，且必须物理嵌套在它所属的 <section> 标签内。
4. **属性完整性**：在关键容器上强制使用 data-type 属性，取值范围仅限：["metadata", "abstract", "section", "figure", "table", "reference"]。

### ⚠️ 严格输出限制（违反将被视为失败）
- **仅输出 HTML 代码**：严禁输出任何解释性文字、开场白（如 "Here is the code..."）、结束语或思维过程。
- **禁止 Markdown 格式**：不要将代码包裹在 ```html 或 ``` 块中，直接以 <!DOCTYPE html> 开头输出纯文本。
- **内容保全**：严禁删除、修改或简化任何原始文本内容。
- **单一文件**：通过 CDN 引入 Tailwind，输出为一个独立的 HTML 文件。

---
以下是原始绝对定位 HTML 代码：
{absolute_html}
"""
    prompt_content = f"""
你是一位顶级的全栈工程师，专精于将复杂的视觉海报逆向工程为"结构化、语义化"的响应式 HTML。你的目标是确保生成的代码不仅在视觉上完美还原，且能通过脚本轻松提取为学术 PlanJSON 格式。

### 输入数据
1. **海报原图**：作为布局和语义逻辑的最终判定标准。
2. **绝对定位 HTML 源码**：提供原始内容、图片 ID (data-fig-id) 及像素级坐标参考。

### 任务要求：遵循以下 Chain-of-Thought (CoT) 逻辑分析

#### 步骤 1：空间与并列关系扫描
- **全局分栏识别**：通过图片识别海报的大框架,确认海报的页眉和页脚区域，正文的panel布局(例如三列布局，两行三列布局等)。
- **全局分块尺寸识别**:通过上一步识别出海报的整体布局后，你需要通过海报图片来分析各个布局的大小比例关系，不能简单的认为是均分或相等关系。
- **横向并列判定**：针对海报中的文本框或图片等元素，你需要仔细观察图片信息，并在必要时检查 HTML 源码中元素的坐标信息来确认元素之间的相对位置关系是横向排列还是纵向排列，严禁不经观察就将相邻元素进行纵向排列。
- **语义分块**：根据原图标题，将海报划分为 Introduction, Methodology 等逻辑章节。

#### 步骤 2：字体层级视觉估算（新增）
基于海报原图进行字体大小的视觉推断，建立全局字体比例体系，**不得凭空假设，必须以图片为唯一视觉依据**：

- **基准确立**：
  - 识别海报中占据最大面积的正文段落文字，将其视觉高度定义为基准字号 `1rem`（通常对应实际渲染的 `14px` 或 `16px`）。
  - 在 HTML `<html>` 根元素上通过内联样式或 Tailwind 的 `text-base` 锚定这一基准。

- **层级比例推断**：观察原图，按以下顺序逐级推断各类文字与基准正文的**视觉高度倍率**，并映射为对应的 Tailwind 字号类：

  | 层级 | 典型元素 | 推断方式 | 映射 Tailwind 类 |
  |---|---|---|---|
  | 海报主标题 | `<h1>` | 目测约为正文的 N 倍高 | `text-4xl` / `text-5xl` |
  | 章节标题 | `<h2>` | 目测约为正文的 N 倍高 | `text-2xl` / `text-3xl` |
  | 子标题 | `<h3>` | 目测约为正文的 N 倍高 | `text-xl` / `text-lg` |
  | 正文段落 | `<p>` | 基准 1 倍 | `text-sm` / `text-base` |
  | 图注/参考文献 | `<figcaption>`, ref | 目测小于正文 | `text-xs` / `text-sm` |

- **字重与间距感知**：
  - 若原图中标题文字笔画明显粗于正文，对应元素添加 `font-bold` 或 `font-semibold`。
  - 若原图中段落行间距视觉宽松，对应元素添加 `leading-relaxed` 或 `leading-loose`；若紧凑，使用 `leading-tight`。

- **一致性约束**：同一语义层级的所有元素必须使用相同字号类，禁止同层级出现两种不同 `text-*` 大小。

#### 步骤 3：结构化 HTML 约束 (面向 PlanJSON 提取)
- **容器化 (Wrapping)**：必须使用 `<section id="section_n">` 包裹每个独立章节。
- **层级分明**：章节标题统一使用 `<h2>`，子标题使用 `<h3>`，正文使用 `<p>`。
- **数据锚点注入**：
    - 必须为每个 `<img>` 或其容器保留原始的 `data-fig-id`。
    - 在关键容器上标注 `data-type` (如 "abstract", "reference", "figure")。
- **数学公式渲染**：必须在 <head> 中配置 MathJax 以解析 LaTeX 公式。请务必包含以下脚本：
    <script>
      window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }} }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
- **线性阅读顺序**：确保源码中的元素顺序符合人类逻辑，而非 OCR 识别的随机顺序。

#### 步骤 4：响应式布局实现 (Tailwind CSS)
- 移除所有 `position: absolute`。
- 使用 `grid` 或 `flex` 替代坐标。在桌面端 (lg) 强制保留横向并排结构，在移动端 (md 以下) 自动垂直堆叠。
- **字体应用**：将步骤 2 中推断出的字号类、字重类、行高类完整应用到对应元素上，不得遗漏。

### 输出约束
- 关注 **Layout**（布局、间距、对齐）和 **Typography**（字号、字重、行高）。
- 忽略颜色、背景、边框等装饰性样式。
- **严禁删除任何原始文本内容。**

### ⚠️ 面向 PlanJSON 提取的终极硬约束：
1. **语义树结构**：HTML 必须呈现 [Header(Metadata)] -> [Main(Sections)] -> [Footer(References)] 的层级。
2. **章节唯一性**：每个学术章节必须包裹在 <section id="section_n"> 中，其中 n 是从 1 开始的递增整数。
3. **图文关联**：所有的图片 (<img>) 必须带有原始的 data-fig-id，且必须物理嵌套在它所属的 <section> 标签内。
4. **属性完整性**：在关键容器上强制使用 data-type 属性，取值范围仅限：["metadata", "abstract", "section", "figure", "table", "reference"]。

### ⚠️ 严格输出限制（违反将被视为失败）
- **仅输出 HTML 代码**：严禁输出任何解释性文字、开场白（如 "Here is the code..."）、结束语或思维过程。
- **禁止 Markdown 格式**：不要将代码包裹在 ```html 或 ``` 块中，直接以 <!DOCTYPE html> 开头输出纯文本。
- **内容保全**：严禁删除、修改或简化任何原始文本内容。
- **单一文件**：通过 CDN 引入 Tailwind，输出为一个独立的 HTML 文件。

---
以下是原始绝对定位 HTML 代码：
{absolute_html}
"""
    prompt_content = f"""
你是一位顶级的全栈工程师，专精于将复杂的视觉网页逆向工程为"结构化、语义化"的响应式 HTML。你的目标是确保生成的代码不仅在视觉上完美还原，且能通过脚本轻松提取为学术 PlanJSON 格式。

### 输入数据
1. **前端网页原图**：作为布局和语义逻辑的最终判定标准。
2. **绝对定位 HTML 源码**：提供原始内容、图片 ID (data-fig-id) 及像素级坐标参考。

### 任务要求：遵循以下 Chain-of-Thought (CoT) 逻辑分析

#### 步骤 1：空间与并列关系扫描
- **全局分栏识别**：通过图片识别网页的大框架,确认网页的panel布局(例如单栏布局、多栏布局等)。
- **全局分块尺寸识别**:通过上一步识别出网页的整体布局后，你需要通过网页图片来分析各个布局的大小比例关系，不能简单的认为是均分或相等关系。
- **横向并列判定**：针对网页中的文本框或图片等元素，你需要仔细观察图片信息，并在必要时检查 HTML 源码中元素的坐标信息来确认元素之间的相对位置关系是横向排列还是纵向排列，严禁不经观察就将相邻元素进行纵向排列。
- **语义分块**：根据原图标题，将网页划分为 Introduction, Methodology 等逻辑章节。

#### 步骤 2：字体层级视觉估算（新增）
基于网页原图进行字体大小的视觉推断，建立全局字体比例体系，**不得凭空假设，必须以图片为唯一视觉依据**：

- **基准确立**：
  - 识别网页中占据最大面积的正文段落文字，将其视觉高度定义为基准字号 `1rem`（通常对应实际渲染的 `14px` 或 `16px`）。
  - 在 HTML `<html>` 根元素上通过内联样式或 Tailwind 的 `text-base` 锚定这一基准。

- **层级比例推断**：观察原图，按以下顺序逐级推断各类文字与基准正文的**视觉高度倍率**，并映射为对应的 Tailwind 字号类：

  | 层级 | 典型元素 | 推断方式 | 映射 Tailwind 类 |
  |---|---|---|---|
  | 网页主标题 | `<h1>` | 目测约为正文的 N 倍高 | `text-4xl` / `text-5xl` |
  | 网页标题 | `<h2>` | 目测约为正文的 N 倍高 | `text-2xl` / `text-3xl` |
  | 子标题 | `<h3>` | 目测约为正文的 N 倍高 | `text-xl` / `text-lg` |
  | 正文段落 | `<p>` | 基准 1 倍 | `text-sm` / `text-base` |
  | 图注/参考文献 | `<figcaption>`, ref | 目测小于正文 | `text-xs` / `text-sm` |

- **字重与间距感知**：
  - 若原图中标题文字笔画明显粗于正文，对应元素添加 `font-bold` 或 `font-semibold`。
  - 若原图中段落行间距视觉宽松，对应元素添加 `leading-relaxed` 或 `leading-loose`；若紧凑，使用 `leading-tight`。

- **一致性约束**：同一语义层级的所有元素必须使用相同字号类，禁止同层级出现两种不同 `text-*` 大小。

#### 步骤 3：结构化 HTML 约束 (面向 PlanJSON 提取)
- **容器化 (Wrapping)**：必须使用 `<section id="section_n">` 包裹每个独立章节。
- **层级分明**：章节标题统一使用 `<h2>`，子标题使用 `<h3>`，正文使用 `<p>`。
- **数据锚点注入**：
    - 必须为每个 `<img>` 或其容器保留原始的 `data-fig-id`。
    - 在关键容器上标注 `data-type` (如 "abstract", "reference", "figure")。
- **数学公式渲染**：必须在 <head> 中配置 MathJax 以解析 LaTeX 公式。请务必包含以下脚本：
    <script>
      window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }} }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
- **线性阅读顺序**：确保源码中的元素顺序符合人类逻辑，而非 OCR 识别的随机顺序。

#### 步骤 4：响应式布局实现 (Tailwind CSS)
- 移除所有 `position: absolute`。
- 使用 `grid` 或 `flex` 替代坐标。在桌面端 (lg) 强制保留横向并排结构，在移动端 (md 以下) 自动垂直堆叠。
- **字体应用**：将步骤 2 中推断出的字号类、字重类、行高类完整应用到对应元素上，不得遗漏。

### 输出约束
- 关注 **Layout**（布局、间距、对齐）和 **Typography**（字号、字重、行高）。
- 忽略颜色、背景、边框等装饰性样式。
- **严禁删除任何原始文本内容。**

### ⚠️ 面向 PlanJSON 提取的终极硬约束：
1. **语义树结构**：HTML 必须呈现 [Header(Metadata)] -> [Main(Sections)] -> [Footer(References)] 的层级。
2. **章节唯一性**：每个学术章节必须包裹在 <section id="section_n"> 中，其中 n 是从 1 开始的递增整数。
3. **图文关联**：所有的图片 (<img>) 必须带有原始的 data-fig-id，且必须物理嵌套在它所属的 <section> 标签内。
4. **属性完整性**：在关键容器上强制使用 data-type 属性，取值范围仅限：["metadata", "abstract", "section", "figure", "table", "reference"]。

### ⚠️ 严格输出限制（违反将被视为失败）
- **仅输出 HTML 代码**：严禁输出任何解释性文字、开场白（如 "Here is the code..."）、结束语或思维过程。
- **禁止 Markdown 格式**：不要将代码包裹在 ```html 或 ``` 块中，直接以 <!DOCTYPE html> 开头输出纯文本。
- **内容保全**：严禁删除、修改或简化任何原始文本内容。
- **单一文件**：通过 CDN 引入 Tailwind，输出为一个独立的 HTML 文件。

---
以下是原始绝对定位 HTML 代码：
{absolute_html}
"""
    prompt_content=f""""
你是一位顶级的全栈工程师，专精于将复杂的视觉网页逆向工程为"结构化、语义化"的响应式 HTML。你的目标是确保生成的代码不仅在视觉上完美还原，且能通过脚本轻松提取为学术 PlanJSON 格式。

## 输入数据
前端网页原图：作为布局和语义逻辑的最终判定标准。

绝对定位 HTML 源码：提供原始内容、图片 ID (data-fig-id) 及像素级坐标参考。

## 任务要求：遵循以下 Chain-of-Thought (CoT) 逻辑分析

### 步骤 1：空间与并列关系扫描
全局分栏识别：通过图片确认网页的 Panel 布局（如单栏、多栏等）。

全局分块尺寸识别：通过图片分析各个布局的大小比例，严禁简单均分。

横向并列判定：仔细观察图片并参考坐标，确认元素相对位置是横向排列还是纵向排列，严禁盲目垂直堆叠。

语义分块：根据原图内容，将网页划分为 Metadata, Introduction, Methodology 等逻辑章节。

### 步骤 2：字体层级视觉估算
基于网页原图进行字体大小的视觉推断，建立全局字体比例体系：

基准确立：识别正文段落，定义为 1rem（对应 text-base）。

层级比例映射：

主标题 <h1> -> text-4xl 或 text-5xl。

章节标题 <h2> -> text-2xl 或 text-3xl。

子标题 <h3> -> text-xl 或 text-lg。

图注/参考文献 -> text-xs 或 text-sm。

字重与间距：标题添加 font-bold；根据视觉宽松度添加 leading-relaxed 或 leading-tight。

### 步骤 3：结构化 HTML 语义约束 (面向 PlanJSON 提取的核心硬约束)
1. 整体架构：

遵循 [Header(Metadata)] -> [Main(Sections)] 的扁平层级。

Metadata 区块：使用 <header data-type="metadata">。

标题：使用 <h1>。

作者：使用 <div data-type="authors"> 包裹，每个作者必须用 <span> 独立分割（如 <span>Lilang Lin</span>）。

机构：使用 <div data-type="organizations">。

其他文本：Metadata 区域内的其他描述性文字（如会议名称、备注）必须包含在内，以便解析至 contents 字段。

交互按钮：如 Github、Arxiv 链接，必须设置为 <nav> 块，内部使用若干 <a> 标签，href 统一使用 #。

2. 章节 (Sections) 约束：

除 Metadata 外，所有学术章节必须包裹在 <section id="section_n" data-type="section"> 中，n 是从 1 开始递增的整数。

每个 Section 的标题统一使用 <h2>，子标题使用 <h3>。

严禁使用 footer、label、input、button 等标签。所有的交互式组件、表单或页脚内容必须转换为普通的 <section> 块，其中的按钮或输入框提示文字必须处理为 <p> 标签。

3. 正文与图文内容：

文本提取：正文内容支持 <p>, <h3>, <h4>, <h5>, <h6> 以及 <pre>。对于代码或 BibTeX 引用，必须使用 <pre> 以保留格式。

图表容器化：图片或表格必须包裹在 <div> 中。

图表判定：根据内容判定 data-type 为 "figure" 或 "table"。

标题绑定：标题文字必须包含在同一个 <div> 内，且标记为 <p data-type="caption">。

组图规范：若是并排组图，图片容器标记为 data-type="figure-group"，标题容器标记为 data-type="caption-group"，确保内部元素索引对应。

ID 保留：所有 <img> 必须保留原始的 data-fig-id。

4. 数学公式：

必须在 <head> 中配置 MathJax：

步骤 4：响应式布局实现 (Tailwind CSS)
移除所有 position: absolute，使用 grid 或 flex 替代坐标。

在桌面端 (lg) 强制保留横向并排结构，在移动端自动垂直堆叠。

⚠️ 严格输出限制
仅输出 HTML 代码：严禁输出任何解释性文字、开场白或结束语。

禁止 Markdown 格式：不要将代码包裹在 ``` 块中，直接以 <!DOCTYPE html> 开头输出。

内容保全：严禁删除、修改或简化任何原始文本内容。

单一文件：通过 CDN 引入 Tailwind，输出为一个独立的 HTML 文件。

以下是原始绝对定位 HTML 代码：
{absolute_html}
    """
    base64_image = get_verified_base64_image(image_path)
    message = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_content
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }
]
    resp = client.chat.completions.create(
        model=model_name,  # 或任意你想试的 Gemini 模型
        messages=message,
        temperature=0
    )
    return resp.choices[0].message.content

def batchImagesGenerate(images_dir, mineru_path, output_dir):
    """
    批量处理图片文件夹中的所有图片。
    - images_dir: 存放原始海报图片的文件夹路径
    - mineru_path: mineru 解析结果的根路径
    - output_dir: 所有结果文件夹的输出根路径
    """
    images_dir = Path(images_dir)
    mineru_path = Path(mineru_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 支持的图片格式
    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

    for image_path in images_dir.iterdir():
        if image_path.suffix.lower() not in image_extensions:
            continue

        poster_name = image_path.stem
        print(f"[Processing] {poster_name}")

        # 创建与图片同名的输出文件夹
        poster_output_dir = output_dir / poster_name
        poster_output_dir.mkdir(parents=True, exist_ok=True)

        # 1. 生成 HTML 并保存
        try:
            html_code = responsiveHTMLGenerate(str(image_path), str(mineru_path))
            html_output_path = poster_output_dir / f"{poster_name}.html"
            save_html(str(html_output_path), html_code)
            print(f"  [✓] HTML saved: {html_output_path}")
        except Exception as e:
            print(f"  [✗] HTML generation failed for {poster_name}: {e}")
            continue

        # 2. 从 mineru 输出中复制子图资源
        visuals_root = mineru_path / poster_name / "visuals"
        sub_dirs = ["equations", "images", "tables"]

        for sub in sub_dirs:
            src_dir = visuals_root / sub
            if not src_dir.exists():
                print(f"  [!] Skipping missing dir: {src_dir}")
                continue

            dst_dir = poster_output_dir 
            dst_dir.mkdir(parents=True, exist_ok=True)

            for file in src_dir.iterdir():
                if file.is_file():
                    shutil.copy2(file, dst_dir / file.name)

            print(f"  [✓] Copied {sub}: {src_dir} -> {dst_dir}")
     

if __name__=="__main__":
    img_path="../small_batch_data/Flexible Attention-Based Multi-Policy Fusion for Efficient Deep Reinforcement Learning_poster.jpg"
    mineru="../posterData/mineru_output"
    output_path="../smallBatch_result/Flexible Attention-Based Multi-Policy Fusion for Efficient Deep Reinforcement Learning_poster.html"
    #poster_name=Path(img_path).stem

    #html_code = responsiveHTMLGenerate(img_path,mineru)
    #save_html(f"{poster_name}_claude.html",html_code)
    #batchImagesGenerate(img_path,mineru,output_path)
    html_code= responsiveHTMLGenerate(img_path,mineru)
    save_html(output_path,html_code)

