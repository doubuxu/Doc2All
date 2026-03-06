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
dotenv.load_dotenv()
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

def build_images_message(images_path,tables_path):#构建图片的name，base64，尺寸等信息数据
    #images_path=get_figures_path(images)
    #tables_path=get_tables_path(images)
    image_list=images_path+tables_path
    image_contents=[]
    for img in image_list:
        b64=image_encode(img[1])
        w,h=get_image_size(img[1])
        image_contents.append({
            "fig_id":img[0],
            "base64":b64,
            "width":f"{w}px",
            "height":f"{h}px"
        })
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

    image_contents=build_images_message(images_path,tables_path)
    multimodal_content=build_multimodal_prompt(image_contents)
    content_list_path=Path(sub_image_path) / poster_name / f"{poster_name}_content_list.json"
    content_list = load_json(content_list_path)
    
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
        <img src="./logo.png" style="width:100px; height:50px;" data-semantic="大学校徽 Logo">
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
  - `src`：必须指向子图文件名（如 `./table_1.png` 或 `./fig_1.jpg`）。
  - `style`：必须内联显式指定宽高，格式为 `style="width: 100px; height: 50px;"`（脚本通过正则提取数字）。
  - **`data-semantic`**：必须添加此属性，用一句话描述图表的具体内容（如：“消融实验数据对比表”）。
- **判定逻辑**：如果文件名包含 "table"，脚本会自动归类为 tables，否则归类为 figures。

### 布局精度要求
- **全局容器**：根容器为 `div#poster-canvas`，宽高需与原图一致。
- **多栏布局**：使用 `main` 标签作为主体，内部划分若干 `.column`。
- **位置对齐**：严格参考 MinerU 的 bbox 坐标，通过 flex/grid 确保元素顺序与物理位置对齐。

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
        <img src="./logo.png" style="width: 100px; height: 100px;" data-semantic="校徽">
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
    message=[
        {"role": "system", "content": """你是一个资深的前端布局工程师。你擅长使用现代 CSS Flexbox 技术复刻复杂的学术海报布局。
你的代码风格要求：
1. 必须使用 Flexbox (display: flex) 处理多栏布局。
2. 严禁使用 <table>、<float> 或过度的 position: absolute。
3. 代码结构必须语义化，通过容器嵌套来表达层级逻辑。
4. 所有布局参数（gap, width, padding）必须参考视觉特征和 bbox 坐标。"""},

        {"role": "user", "content":[
            {"type":"text","text":prompt},
            {"type":"text","text":"我将给出海报的图片，以及海报中分割出来的图像和表格，请根据这些内容生成对应的HTML数据。"},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image_encode(poster_file)}"
                }
            },
            *multimodal_content,
            {
                "type":"text",
                "text":"我将给出mineru版面识别的content_list.json结果，内容是mineru识别的元素阅读顺序和个元素的bbox等信息，请你参考该json(特别是bbox这一位置信息)来辅助生成最终的html代码"
            },
            {
                "type":"text",
                "text":content_list
            }
            ]
        }
    ]
    print(message)
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
    img_path="./[Re] Graph Edit Networks_poster.jpg"
    poster_name=Path(img_path).stem
    print(poster_name)
    sub_image_path=f'./output'
    html_code=singele_poster_process(img_path,poster_name,sub_image_path)
    print(html_code)
    html_path=f'./{poster_name}3.html'
    save_html(html_path,html_code)