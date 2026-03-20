# 1. 安装依赖（仅需一次）
# pip install openai
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from pathlib import Path
from utils.JsonTools import load_json,save_json
from utils.htmlTools import *
from openai import OpenAI
import base64
from PIL import Image 
import dotenv
import json
dotenv.load_dotenv()

import copy

def rescale_content_list(content_list, middle_json, img_w, img_h):
    """
    根据 middle.json 中的 page_size 将 content_list 的坐标缩放到图片像素尺寸
    
    Args:
        content_list: 待修改的 content_list 列表
        middle_json: MinerU 输出的完整 JSON 字典（包含 pdf_info 和 page_size）
        img_w: 原始海报图片的像素宽度
        img_h: 原始海报图片的像素高度
        
    Returns:
        修改完 bbox 的 content_list
    """
    # 1. 从 middle_json 中安全获取 page_size
    # 假设处理的是第一页 (page_idx: 0)
    try:
        pdf_w, pdf_h = middle_json["pdf_info"][0]["page_size"]
    except (KeyError, IndexError):
        print("Error: 无法从 middle_json 中找到 page_size")
        return content_list

    # 2. 计算缩放比例
    scale_x = img_w / pdf_w
    scale_y = img_h / pdf_h

    def rescale_bbox(bbox):
        """内部辅助函数：执行具体的缩放计算"""
        if not bbox or len(bbox) != 4:
            return bbox
        return [
            int(bbox[0] * scale_x),
            int(bbox[1] * scale_y),
            int(bbox[2] * scale_x),
            int(bbox[3] * scale_y)
        ]

    def process_recursive(item):
        """递归遍历并修改所有包含 bbox 的字典"""
        if isinstance(item, dict):
            # 如果当前字典有 bbox 字段，直接修改
            if "bbox" in item:
                item["bbox"] = rescale_bbox(item["bbox"])
            
            # 递归处理字典中的所有 key (如 lines, spans, blocks 等)
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    process_recursive(value)
        elif isinstance(item, list):
            # 如果是列表，遍历列表中的每一项
            for element in item:
                process_recursive(element)

    # 3. 深拷贝原始数据并执行递归修改
    new_content_list = copy.deepcopy(content_list)
    process_recursive(new_content_list)

    return new_content_list

def restore_bbox_to_pixel(content_list, img_w, img_h):
    import copy
    new_list = copy.deepcopy(content_list)
    
    def process_item(item):
        if "bbox" in item:
            x0, y0, x1, y1 = item["bbox"]
            # 还原公式： 坐标 * 实际尺寸 / 1000
            item["bbox"] = [
                int(x0 * img_w / 1000),
                int(y0 * img_h / 1000),
                int(x1 * img_w / 1000),
                int(y1 * img_h / 1000)
            ]
        # 递归处理子层级 (lines, spans 等)
        for key in ["lines", "spans", "para_blocks", "list_items"]:
            if key in item and isinstance(item[key], list):
                for sub_item in item[key]:
                    if isinstance(sub_item, dict):
                        process_item(sub_item)
    
    for entry in new_list:
        process_item(entry)
    return new_list

def minimize_content_plan(content_plan):
    """
    输入: content_plan (list[dict])，类似题目中的json结构
    输出: 删除 page_idx / img_path / table_body 后的精简json
    """
    
    remove_keys = {"page_idx", "img_path", "table_body"}
    minimized = []

    for item in content_plan:
        new_item = {}
        for key, value in item.items():
            if key not in remove_keys:
                new_item[key] = value
        minimized.append(new_item)

    return minimized



def image_encode(img_path):
        with open(img_path, "rb") as f:
            img_data = f.read()
        encoded_str = base64.b64encode(img_data).decode("utf-8")
        return encoded_str

def get_image_size(path):
    w, h = Image.open(path).size
    return w,h


def get_figures_path(output_dir, file_name):#获取海报中所有图片的路径
    file_name=file_name
    image_dict_path=Path(output_dir)/file_name/"dict"/"images.json"
    images_path=[]
    image_dict=load_json(image_dict_path)
    for img in image_dict:
        images_path.append([img["fig_id"],img["path"]])
    return images_path

def get_tables_path(output_dir, file_name):#获取海报中所有表格的路径
    file_name=file_name
    table_dict_path=Path(output_dir)/file_name/"dict"/"tables.json"
    tables_path=[]
    table_dict=load_json(table_dict_path)
    for table in table_dict:
        tables_path.append([table["table_id"],table["path"]])
    return tables_path

def get_bbox_by_img_path(content_list, img_path):
    """
    根据 img_path 在 content_list 中查找对应的 bbox
    """
    for item in content_list:
        if item.get("img_path") == img_path:
            return item.get("bbox")
    return None

def build_images_message(images_path,tables_path,content_list):#构建图片的name，base64，尺寸等信息数据
    #images_path=get_figures_path(images)
    #tables_path=get_tables_path(images)
    image_list=images_path+tables_path
    image_contents=[]
    for img in image_list:
        b64=image_encode(img[1])
        w,h=get_image_size(img[1])
        bbox = get_bbox_by_img_path(content_list,img[1])
        image_contents.append({
            "fig_id":img[0],
            "base64":b64,
            "width":f"{w}px",
            "height":f"{h}px",
            "bbox" : f"{bbox}"
        })
    return image_contents

import copy

def get_clean_image_contents(image_contents):
    """
    删除 image_contents 中每个条目的 base64 字段，
    防止构建提示词时导致上下文过长。
    """
    # 使用深拷贝防止修改原始列表
    cleaned_contents = copy.deepcopy(image_contents)
    
    for item in cleaned_contents:
        # 使用 pop 删除键，如果不存在也不会报错
        item.pop("base64", None)
        
    return cleaned_contents

# 使用示例
# image_contents_for_prompt = get_clean_image_contents(image_contents)

import os
from openai import OpenAI


def add_semantic_info(image_contents):
    """
    输入: image_contents (list[dict])
    输出: 在每个元素中新增 'semantic-info' 字段
    """

    api = os.getenv("API_KEY")
    url = os.getenv("BASE_URL")
    model_name = os.getenv("SEMANTIC_MODEL", "qwen3-max")

    client = OpenAI(
        api_key=api,
        base_url=url
    )

    for img in image_contents:
        base64_img = img["base64"]

        message = [
            {
                "role": "system",
                "content": "You are a vision assistant that summarizes the semantic content of figures"
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please describe the semantic content of this image in a concise sentence."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_img}"
                        }
                    }
                ]
            }
        ]

        resp = client.chat.completions.create(
            model=model_name,
            messages=message,
            temperature=0
        )

        semantic_info = resp.choices[0].message.content

        img["semantic-info"] = semantic_info

    return image_contents

def build_multimodal_prompt(images):#构建多模态输入的prompt
    """
    images: list of dict, e.g. [
        {"base64": "...", "filename": "a.jpg", "width": 800, "height": 600},
        ...
    ]
    """
    content = [{"type": "text", "text": f"我将上传 {len(images)} 张海报中的子图，信息如下："}]
    
    for idx, img in enumerate(images, 1):
        # 插入元数据描述
        meta_text = f"'文件名':{img['fig_id']} 'width':'{img['width']}' 'height':'{img['height']}'"
        content.append({"type": "text", "text": meta_text})
        
        # 插入图片
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img['base64']}",
                # 如有 detail 参数也放这里
            }
        })
    return content



def singele_poster_process(poster_path,poster_name,sub_image_path)->str:

    poster_file=Path(poster_path)

    images_path=get_figures_path(sub_image_path,poster_name)
    tables_path=get_tables_path(sub_image_path,poster_name)

    
    #multimodal_content=build_multimodal_prompt(image_contents)
    content_list_path=Path(sub_image_path) / poster_name / f"{poster_name}_content_list.json"
    layout_path = Path(sub_image_path) / poster_name / f"{poster_name}_middle.json"
    content_list = load_json(content_list_path)
    #middle_json = load_json(layout_path)
    w,h=get_image_size(poster_file)
    content_list = restore_bbox_to_pixel(content_list,w,h)
    image_contents=build_images_message(images_path,tables_path,content_list)
    image_contents = add_semantic_info(image_contents)
    image_contents = get_clean_image_contents(image_contents)
    content_list = minimize_content_plan(content_list)

    print("image_contents")
    print(image_contents)
    print("content_list")
    print(content_list)


    prompt="""
我将给出原始海报的图片和海报中的子图(包括图片和表格)以及这些图片对应的尺寸信息，请根据这些信息输出能表达海报布局信息的html代码
请注意以下几点：
1. 最终通过html生成的海报在布局上要与海报图片一致,并且最终生成的海报不能有大面积的多余留白。
2. 最终通过html生成的海报中的子图(包括图片和表格)尺寸要与我给出的子图尺寸保持一致，在html中通过相对路径的形式表示子图，例如'./fig_1.jpg'。如果海报中存在我没有给出的子图，则忽略这些子图，留白即可。
3. 对于海报中的标题、文本和公式等文本信息，你要严格遵循原图中的信息，结合我给出的content_list.json进行提取，不得对文本信息做修改、删减或增加等操作。
4. 对于文本信息的换行、字体大小和行间距等影响布局的因素，你要严格遵循原始海报中的设置，保证通过html表示的海报中的一段文本和原图中对应的文本所占的面积相等。
5. 你的核心任务是一比一复刻原图的布局信息，不得做任何修改和优化。例如原图中两张图是横向排列，那么html中就必须是横向排列。
6. 对于图片和表格的caption，你要一字不差的提取其文本信息，并遵循原图保持和图片的相对位置。
7. 不要遗漏任何文本、公式、图片或表格信息
8. 你的任务是识别并复现学术海报的布局信息，不需要生成任何style相关的信息，例如颜色等。但字体等影响布局的信息必须判断并生成。
9. 你只需要生成可以直接在浏览器中展示的html代码，不要输出任何多余的字符。
10. 请你仔细比对子图和海报的内容，出现在子图中的任何信息都用子图占位符表示，不需要在html的其余部分展示，避免信息重复。例如子图中包括了图片本身和图片的caption，那么你就不必另外生成caption，否则会和子图中的caption重复。
"""
    prompt = """
### 任务目标
你是一个顶尖的前端布局专家。你的任务是根据提供的【海报原图】、【子图列表（含尺寸）】以及【MinerU 版面分析 JSON (含 bbox)】，编写一段单文件的 HTML 代码，1:1 复刻海报的物理布局。

### 核心布局协议 (必须遵守)
为了确保布局精准且易于解析，请遵循以下 HTML 结构规范：

1. **全局容器**：使用一个固定宽高的 `div#poster-canvas` 作为根容器，尺寸严格设置为海报原图尺寸。
2. **多栏架构**：根据原图视觉效果，使用 `display: flex` 或 `grid` 将 `main` 划分为若干 `.column`。
3. **语义化 Section**：每个逻辑区块必须包裹在 `<section class="layout-block" data-section-id="section_n">` 中。
4. **标题识别**：每个 section 内部的标题必须使用 `<h2 class="section-header">`。
5. **内容载体**：
   - 纯文本：包裹在 `<p class="text-block">` 中。
   - 列表：使用 `<ul><li class="list-item">` 结构。
   - 公式：使用 `div.equation` 并在内部书写 LaTeX。
6. **图表占位**：
   - 使用 `<div class="figure-container">` 承载图片。
   - 必须包含 `<img>` 标签，`src` 使用子图文件名（如 `./fig_1.jpg`）。
   - 图片尺寸必须通过内联 style 显式指定，例如：`style="width: 280px; height: 62px;"`。
   - 如果子图中已包含 caption，HTML 中不得重复生成文本。

### 布局精度要求
- **BBox 对齐**：严格参考 content_list.json 中的 `bbox` 坐标。确保 HTML 元素的物理相对位置、排列顺序与 bbox 反映的逻辑一致。
- **空白控制**：利用 `margin`、`padding` 和 `gap` 消除不必要的留白，使元素分布密度与原图一致。
- **文本流**：通过设置 `font-size` 和 `line-height`（参考原图比例），确保文本块的视觉面积与原图对齐。

### Flexbox 布局规范：
1. 根容器使用 `display: flex; flex-direction: column;`。
2. 头部（Header）和主体（Main）作为根容器的直接子元素。
3. 主体（Main）必须设置为 `display: flex; flex-direction: row;`，并根据原图划分出若干 `.column` 容器。
4. 每个 `.column` 内部使用 `display: flex; flex-direction: column;` 来垂直排列各个 `.layout-block`。
5. 使用 `gap` 属性来控制列间距和块间距，严禁使用硬编码的换行符来挤占空间。

### 禁令
- 严禁修改、增删、润色任何文本内容。
- 严禁生成任何背景颜色、边框阴影等装饰性 style。
- 严禁输出 Markdown 格式，直接输出以 `<!DOCTYPE html>` 开头的代码字符串。

### 示例结构
<section class="layout-block" data-section-id="section1">
    <h2 class="section-header">标题内容</h2>
    <p class="text-block">正文内容...</p>
    <div class="figure-container">
        <img src="./fig_1.jpg" style="width: 274px; height: 82px;">
    </div>
</section>
"""
    prompt = """
### 任务目标
你是一个顶尖的前端布局专家。你的任务是根据提供的【海报原图】、【子图列表（含尺寸）】以及【MinerU 版面分析 JSON (含 bbox)】，编写一段单文件的 HTML 代码，1:1 复刻海报的物理布局。

### 核心布局协议 (必须遵守)
为了确保布局精准且易于解析，请遵循以下 HTML 结构规范：

1. **全局容器**：使用一个固定宽高的 `div#poster-canvas` 作为根容器，尺寸严格设置为海报原图尺寸。
2. **多栏架构**：根据原图视觉效果，使用 `display: flex` 或 `grid` 将 `main` 划分为若干 `.column`。
3. **语义化 Section**：每个逻辑区块必须包裹在 `<section class="layout-block" data-section-id="section_n">` 中。
4. **标题识别**：每个 section 内部的标题必须使用 `<h2 class="section-header">`。
5. **头部规范 (用于元数据解析)**：
   - 标题必须使用 `<h1 class="poster-title">`。
   - 作者信息必须使用 `<p class="poster-authors">`。
   - 机构信息和 Logo 必须包裹在 `<div class="header-logos">` 中。
6. **内容载体**：
    - 纯文本：包裹在 `<p class="text-block">` 中。
    - 列表：使用 `<ul><li class="list-item">` 结构。
    - 公式：使用 `div.equation` 并在内部书写 LaTeX。
7. **图表占位与语义标注 (核心新增)**：
    - 使用 `<div class="figure-container">` 承载图片。
    - 必须包含 `<img>` 标签，`src` 使用子图文件名。
    - **必须添加 `data-semantic` 属性**：请观察子图内容，用一句准确的中/英文描述该图表表达的核心信息（如：“GEN 模型架构流程图” 或 “实验精度对比折线图”）。
    - 图片尺寸必须通过内联 style 显式指定，例如：`style="width: 280px; height: 62px;"`。
    - 如果子图中已包含 caption，HTML 中不得重复生成文本。

### 布局精度要求
- **BBox 对齐**：严格参考 content_list.json 中的 `bbox` 坐标。确保 HTML 元素的物理相对位置、排列顺序与 bbox 反映的逻辑一致。
- **空白控制**：利用 `margin`、`padding` 和 `gap` 消除不必要的留白，使元素分布密度与原图一致。
- **文本流**：通过设置 `font-size` 和 `line-height`（参考原图比例），确保文本块的视觉面积与原图对齐。

### Flexbox 布局规范：
1. 根容器使用 `display: flex; flex-direction: column;`。
2. 头部（Header）和主体（Main）作为根容器的直接子元素。
3. 主体（Main）必须设置为 `display: flex; flex-direction: row;`，并根据原图划分出若干 `.column` 容器。
4. 每个 `.column` 内部使用 `display: flex; flex-direction: column;` 来垂直排列各个 `.layout-block`。
5. 使用 `gap` 属性来控制列间距和块间距，严禁使用硬编码的换行符来挤占空间。

### 禁令
- 严禁修改、增删、润色任何文本内容。
- 严禁生成任何背景颜色、边框阴影等装饰性 style。
- 严禁输出 Markdown 格式，直接输出以 `<!DOCTYPE html>` 开头的代码字符串。

### 示例结构
<header>
    <h1 class="poster-title">标题内容</h1>
    <p class="poster-authors">作者 A, 作者 B</p>
    <div class="header-logos">
        <img src="./fig_1.png" style="width:100px; height:50px;" data-semantic="大学校徽 Logo">
    </div>
</header>
<main>
    <div class="column">
        <section class="layout-block" data-section-id="section1">
            <h2 class="section-header">章节标题</h2>
            <p class="text-block">正文内容...</p>
            <div class="figure-container">
                <img src="./fig_1.jpg" style="width: 274px; height: 82px;" data-semantic="展示模型准确率的柱状图">
            </div>
        </section>
    </div>
</main>
"""
    prompt = """
### 任务目标
你是一个顶尖的前端布局专家。你的任务是编写一段单文件的 HTML 代码，1:1 复刻海报的物理布局。该 HTML 必须严格遵循以下结构协议，以便后续自动化脚本解析。

### 核心布局协议 (必须严格遵守)

#### 1. 头部元数据 (Metadata)
- **容器**：必须使用 `<header>` 标签。
- **标题**：必须使用 `<h1 class="poster-title">`。
- **作者**：必须使用 `<p class="poster-authors">`，多名作者用逗号分隔。
- **机构与链接**：必须包裹在 `<div class="header-logos">` 中。
  - 机构名称：包裹在 `<div>` 中，脚本会提取其 text。
  - GitHub 链接：包裹在 `<div>` 中，需包含 "github.com" 文本。
  - Logo 图片：使用 `<img>`，必须包含 `data-semantic` 描述其用途。

#### 2. 逻辑区块 (Sections)
- **容器**：每个独立板块必须使用 `<section class="layout-block" data-section-id="section_n">`，其中 `n` 为自增数字。
- **标题**：板块标题必须使用 `<h2 class="section-header">`。
- **内容载体 (直接子元素)**：
  - 正文文本：必须使用 `<p class="text-block">`。
  - 列表项目：必须使用 `<ul>` 嵌套 `<li class="list-item">`。
  - 参考文献：必须使用 `<div class="references-text">`。

#### 3. 图表与表格 (Figures & Tables)
- **容器**：必须包裹在 `<div class="figure-container">` 或 `<div class="row-container">` 中。
- **图片标签**：必须使用 `<img>` 标签。
- **关键属性**：
  - `src`：必须指向子图文件名,后缀为jpg（如 `./table_1.jpg` 或 `./fig_1.jpg`）。
  - **`data-semantic`**：必须添加此属性，用一句话描述图表的具体内容（如：“消融实验数据对比表”）。
- **判定逻辑**：如果文件名包含 "table"，脚本会自动归类为 tables，否则归类为 figures。

### 布局精度要求
- **全局容器**：根容器为 `div#poster-canvas`，宽高需与原图一致。
- **多栏布局**：使用 `main` 标签作为主体，内部划分若干 `.column`。
- **位置对齐**：严格参考 MinerU 的 bbox 坐标，通过 flex/grid 确保元素顺序与物理位置对齐。
- **字体信息**：根据图片中的语义信息和尺寸信息识别不同文本的字体和间距等信息，务必做到布局与图中所示相同。
### 禁令
- 严禁修改类名（Class Name），必须与上述协议完全一致。
- 严禁在 `layout-block` 内部使用不规范的嵌套（如在 `p` 标签外直接裸露文字）。
- 直接输出以 `<!DOCTYPE html>` 开头的代码字符串，严禁任何 Markdown 包裹。

### 正确结构示例
<header>
    <h1 class="poster-title">论文标题</h1>
    <p class="poster-authors">作者A, 作者B</p>
    <div class="header-logos">
        <div>XX 大学</div>
        <div>github.com/project</div>
        <img src="./fig_1.jpg" style="width: 100px; height: 100px;" data-semantic="校徽">
    </div>
</header>
<main>
    <div class="column">
        <section class="layout-block" data-section-id="section_1">
            <h2 class="section-header">引言</h2>
            <p class="text-block">这是正文内容。</p>
            <div class="figure-container">
                <img src="./fig_1.jpg" style="width: 500px; height: 300px;" data-semantic="模型架构图">
            </div>
        </section>
    </div>
</main>
"""
    prompt="""
### 任务目标
你是一个顶尖的前端布局专家。你的任务是编写一段单文件的 HTML 代码，1:1 精准复刻海报的原始物理布局。该 HTML 必须严格遵循以下结构协议，以便后续自动化脚本解析。

### 核心布局协议 (必须严格遵守)

#### 1. 头部元数据 (Metadata)
- **容器**：必须使用 `<header>` 标签。
- **标题**：必须使用 `<h1 class="poster-title">`。
- **作者**：必须使用 `<p class="poster-authors">`，多名作者用逗号分隔。
- **机构与链接**：必须包裹在 `<div class="header-logos">` 中。
  - 机构名称：包裹在 `<div>` 中。
  - GitHub 链接：包裹在 `<div>` 中，需包含 "github.com" 文本。
  - Logo 图片：使用 `<img>`，必须包含 `data-semantic` 描述其用途。

#### 2. 逻辑区块 (Sections)
- **容器**：每个独立板块必须使用 `<section class="layout-block" data-section-id="section_n">`，其中 `n` 为自增数字。
- **标题**：板块标题必须使用 `<h2 class="section-header">`。
- **内容载体**：正文使用 `<p class="text-block">`，列表使用 `<ul>` 嵌套 `<li class="list-item">`。

#### 3. 图表与横向布局 (Crucial: Image & Row Handling)
- **横向并排容器**：**[硬性要求]** 若 Bbox 显示多个元素（如两张对比图、图文并排）处于同一水平高度，必须使用 `<div class="row-container">` 包裹，并在 PC 端使用 `display: flex; flex-direction: row;` 实现并排。
- **图片标签 `<img>` 规范**：
  - **文件名引用**：`src` 属性必须与子图信息json中的名字保持一致，且后缀统一为 `.jpg`（例如 `./fig_1.jpg`, `./table_2.jpg`）。严禁自造文件名。
  - **语义描述**：必须包含 **`data-semantic`** 属性，data-semantic字段的值照搬子图和表格信息中的semantic-info字段（如 `data-semantic="消融实验结果柱状图"`）。
  - **分类判定**：文件名包含 "table" 的放入表格类逻辑，其余归为 figures。
  - **图表覆盖范围**: 你必须根据原始海报视觉信息，参考子图和图表描述信息中的尺寸、位置和语义信息，确认好子图的范围，避免在生成html时重复生成子图中已经存在的文本信息

### 响应式布局与复刻精度要求
- **全局容器**：`div#poster-canvas`，必须设为 `width: 100%; max-width: [原图宽度]px; margin: 0 auto;`。
- **布局逻辑**：严格参考 MinerU 的 `bbox` 坐标。水平邻近元素必须通过 `row-container` 维持左右布局，严禁在宽屏下坍塌为上下堆叠。
- **响应式断点**：必须包含 `@media (max-width: 992px)`，此时 `.column` 和 `.row-container` 切换为 `flex-direction: column`。
- **图片处理**：严禁写死 `width/height`。使用 `aspect-ratio` 锁定比例，CSS 统一设置 `img { max-width: 100%; height: auto; object-fit: contain; }`。
- **内容完整性**：必须逐条核对 `content_list.json`，确保所有 text 文本 100% 还原，严禁遗漏。根据图片视觉特征估算并设定合理的 `font-size` 和 `gap`，估算font-size和gap时要重点参考已知的海报尺寸、子图尺寸等信息来估算。
- **图文布局**：如果文本与图片是横向并列的位置关系，那么html中必须使用 `<div class="row-container">` 包裹，并在 PC 端使用 `display: flex; flex-direction: row;` 实现并排。
- **文本布局**：仔细观察原图中的文本排列，在宽屏模式下不要擅自改变文本的换行位置等影响布局的因素。

### 禁令
- 严禁修改类名（Class Name）。
- 严禁使用 `position: absolute` 定位。
- 严禁在宽屏模式下将原图的左右并排结构拆散。
- 直接输出以 `<!DOCTYPE html>` 开头的代码字符串，严禁任何 Markdown 包裹。

### 正确结构示例
<header>
    <h1 class="poster-title">论文标题</h1>
    <div class="header-logos">
        <img src="./fig_0.jpg" data-semantic="校徽">
    </div>
</header>
<main>
    <div class="column">
        <section class="layout-block" data-section-id="section_1">
            <h2 class="section-header">实验结果</h2>
            <div class="row-container">
                <img src="./fig_1.jpg" data-semantic="对比图左" style="aspect-ratio: 1/1;">
                <img src="./fig_2.jpg" data-semantic="对比图右" style="aspect-ratio: 1/1;">
            </div>
        </section>
    </div>
</main>
"""
    # 在调用前，请确保已经通过 Python 脚本将 content_list 中的 bbox 
# 从 0-1000 还原到了实际像素 (w=3456, h=2304)

    prompt = f"""
### 任务目标
你是一个高精度页面重建专家。你的任务是编写一段“布局施工图”风格的单文件 HTML 代码。
目标是利用提供的像素级坐标，将海报内容 1:1 地“钉”在固定尺寸的画布上。

### 核心规范 
1. **画布设置**：
   - 必须在 `div#poster-canvas` 上设置固定宽高：`width: {w}px; height: {h}px;`。
   - 使用 `position: relative; background: white;`。

2. **定位协议 **：
   - 在此阶段，**必须**使用 `position: absolute;`。
   - 所有的 `left`, `top`, `width`, `height` 必须基于提供的像素级 `bbox` 。
   - 严禁使用 Flex 或 Float。

3. **元数据埋点 **：
   - 每个元素必须包含 `data-raw-bbox` 属性，直接填入 MinerU 原始的 [x0, y0, x1, y1] (0-1000) 坐标。
   - 每个元素必须包含 `data-type` 属性（如 text, image, table, header）。

4. **内容填充**：
   - **文本**：使用 `<span>` 或 `<p>`，根据 bbox 高度推算 `font-size`和gap，必须 100% 还原 content_list 中的 text布局。
   - **图片/表格**：使用 `<img>`，`src` 需对应images_contents中的"fig_id"，文件后缀为jpg，例如./fig_1.jpg必须设置 `object-fit: contain;` 以防变形。
   - **语义描述**：必须包含 **`data-semantic`** 属性，data-semantic字段的值照搬子图和表格信息中的semantic-info字段（如 `data-semantic="消融实验结果柱状图"`）。
   - **缺失信息**：如果原图中出现了提供的子图列表中没有的子图，仍要按指定格式生成<img>，并估算其大小，使用矩形框表示
5. **风格属性**
你的核心任务是复刻图中海报的布局信息，不必复现风格信息，例如字体样式、字体色彩、背景框色彩等信息。
   - **字体设置**：统一使用 font-family: sans-serif;
   - **颜色设置**：文字统一为黑色 (#000000)，背景统一为白色 (#FFFFFF)
### 交付风格示例
<div id="poster-canvas" style="position: relative; width: {w}px; height: {h}px;">
    <h1 data-type="header" data-raw-bbox="[27, 56, 272, 92]" 
        style="position: absolute; left: 93px; top: 129px; width: 846px; height: 83px; font-size: 40px;">
        [Re] Graph Edit Networks
    </h1>
    <p data-type="text" data-raw-bbox="[28, 151, 279, 173]"
       style="position: absolute; left: 96px; top: 347px; width: 867px; height: 50px;">
       Reproduced: Paaβen et. al. (ICLR, 2021)
    </p>
</div>

### 禁令
- 严禁任何形式的简化：不要跳过任何一条 content_list 里的数据。
- 严禁合并：即便两个文本块看起来挨得很近，也必须按 JSON 里的独立 bbox 分别生成标签。
- 直接输出以 `<!DOCTYPE html>` 开头的HTML代码字符串，不要输出任何多余的字符。
"""

    #prompt.replace("[原图宽度]",f"{w}")
    message=[
        {"role": "system", "content": """你是一个资深的前端布局工程师。你擅长使用HTML技术复刻复杂的学术海报布局。
"""},

        {"role": "user", "content":[
            {"type":"text","text":prompt},
            {"type":"text","text":f"下面我将给出海报的图片，以及海报中分割出来的图像和表格的位置、尺寸和语义信息，请根据这些内容生成对应的HTML数据。海报的尺寸是(width:{w}px,height:{h}px)"},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image_encode(poster_file)}"
                }
            },
            {
                "type":"text",
                "text":"我将给出mineru版面识别的content_list.json结果，内容是mineru识别的元素阅读顺序和个元素的bbox等信息，请你参考该json(特别是bbox这一位置信息)来辅助生成最终的html代码。content_list的元素顺序就是海报的阅读顺序。其中的 bbox 坐标已转换为像素单位,与海报尺寸一致。content_list:"
            },
            {
                "type":"text",
                "text":content_list
            },
            {
            "type":"text",
            "text":"下面是从海报中裁剪出的子图和表格的描述信息image_contents(包含bbox、尺寸和semantic-info):"
            },

            {
            "type":"text",
            "text": json.dumps(image_contents, ensure_ascii=False, indent=2)
            }
            ]
        }
    ]
    #print(message)
    with open('./test.txt','w',encoding='utf-8') as f:
        json.dump(message, f, ensure_ascii=False, indent=2)
    api=os.getenv("API_KEY")
    url=os.getenv("BASE_URL")
    model_name=os.getenv("VISUAL_MODEL","qwen3-max")
    client=OpenAI(
        api_key=api,
        base_url=url
    )
    resp = client.chat.completions.create(
        model=model_name,  # 或任意你想试的 Gemini 模型
        messages=message,
        temperature=0
    )
    #save_json(resp.choices[0].message.content,)
    return resp.choices[0].message.content

def poster_html_generate_batch(poster_path,sub_image_path,save_path):
    poster_path=Path(poster_path)
    for item in poster_path.iterdir():
        poster_name=item
        poster_name_with_no_suffix=poster_name[:-4]
        html_data=singele_poster_process(poster_path,poster_name,sub_image_path)
        html_file=save_path/f"{poster_name_with_no_suffix}.html"
        save_json(html_data,html_file)

if __name__ == "__main__":
    """
    img_path="../webData/imgs/AdaMML_ Adaptive Multi-Modal Learning for Efficient Video Recognition.png"
    poster_name=Path(img_path).stem
    print(poster_name)
    sub_image_path=f'../webData/mineru_output'
    html_code=singele_poster_process(img_path,poster_name,sub_image_path)
    print(html_code)
    html_path=f'./{poster_name}_2.html'
    save_html(html_path,html_code)
    """
    img_path="../posterData/Flexible Attention-Based Multi-Policy Fusion for Efficient Deep Reinforcement Learning_poster.jpg"

    poster_name=Path(img_path).stem
    sub_image_path="../posterData/mineru_output"
    html_code=singele_poster_process(img_path,poster_name,sub_image_path)
    html_path=f"./{poster_name}4.html"
    save_html(html_path,html_code)