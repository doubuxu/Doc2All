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


def get_figures_path(single_ppt_path):#获取海报中所有图片的路径
    #file_name=file_name
    #image_dict_path=Path(output_dir)/file_name/"dict"/"images.json"
    images_path_info=[]
    #image_dict=load_json(image_dict_path)
    images_path=Path(single_ppt_path)/"images"
    for item in images_path.iterdir():
        image_name=item.stem
        images_path_info.append([image_name,item])
    
    #for img in image_dict:
    #    images_path.append([img["fig_id"],img["path"]])
    return images_path_info

def get_tables_path(single_ppt_path):#获取海报中所有表格的路径
    #file_name=file_name
    #table_dict_path=Path(output_dir)/file_name/"dict"/"tables.json"
    tables_path_info=[]
    #table_dict=load_json(table_dict_path)
    table_path=Path(single_ppt_path)/"tables"
    for item in table_path.iterdir():
        table_name=item.stem
        tables_path_info.append([table_name,item])
    #for table in table_dict:
    #    tables_path.append([table["table_id"],table["path"]])
    return tables_path_info

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



def singele_poster_process(ppt_path,index)->str:

    #ppt_name=Path(ppt_path).stem
    single_ppt_path=Path(ppt_path)/f"page_{index}"

    images_path=get_figures_path(single_ppt_path)
    tables_path=get_tables_path(single_ppt_path)

    image_contents=build_images_message(images_path,tables_path)
    multimodal_content=build_multimodal_prompt(image_contents)
    content_list_path=Path(single_ppt_path)/"layout.json"
    content_list = load_json(content_list_path)
    ppt_image=Path(single_ppt_path)/"full_slide.png"
   
    WIDTH,HEIGHT=get_image_size(ppt_image)
 
    prompt = """
### 任务目标

你是一个顶尖的前端布局专家。你的任务是编写一段单文件的 HTML 代码，1:1 复刻单页ppt的物理布局。该 HTML 必须严格遵循以下结构协议，以便后续自动化脚本解析。

### 物理布局与画布约束 (强制规则)
固定画布尺寸：本页 PPT 的根容器为 div#ppt-canvas，必须显式设定为宽度 {{WIDTH}}px，高度 {{HEIGHT}}px。

布局刚性：#ppt-canvas 必须设置为 position: relative; overflow: hidden;。

禁止高度坍塌或溢出：无论内容多少，生成的 #ppt-canvas 物理高度必须始终等于 {{HEIGHT}}px。严禁使用 height: auto 或 min-height。如果内容量与固定高度冲突，必须通过缩小字号、压缩间距或调整图片尺寸来适配，严禁撑开容器总高度。

### 核心布局协议 (必须严格遵守)

#### 1. 头部元数据 (Metadata)

* **容器**：必须使用 `<header>` 标签。
* **标题**：必须使用 `<h1 class="ppt-title">`。
* **作者**：必须使用 `<p class="ppt-authors">`，多名作者用逗号分隔。
* **机构与链接**：必须包裹在 `<div class="header-logos">` 中。

  * 机构名称：包裹在 `<div>` 中，脚本会提取其 text。
  * GitHub 链接：包裹在 `<div>` 中，需包含 "github.com" 文本。
  * Logo 图片：使用 `<img>`，必须包含 `data-semantic` 描述其用途。

---

#### 2. 逻辑区块 (Sections)

* **容器**：每个独立板块必须使用 `<section class="layout-block" data-section-id="section_n">`，其中 `n` 为自增数字。
* **标题**：板块标题必须使用 `<h2 class="section-header">`。
* **内容载体 (直接子元素)**：

  * 正文文本：必须使用 `<p class="text-block">`。
  * 列表项目：必须使用 `<ul>` 嵌套 `<li class="list-item">`。
  * 参考文献：必须使用 `<div class="references-text">`。

#### 3. 图表与表格 (Figures & Tables)

* **容器**：必须包裹在 `<div class="figure-container">` 或 `<div class="row-container">` 中。
* **图片标签**：必须使用 `<img>` 标签。
* **关键属性**：

  * `src`：必须指向子图文件名，后缀为 jpg（如 `./slide_0_table_1.jpg` 或 `./slide_1_fig_1.jpg`）。
  * `style`：必须内联显式指定宽高，格式为 `style="width: 100px; height: 50px;"`（脚本通过正则提取数字）。
  * **`data-semantic`**：必须添加此属性，用一句话描述图表的具体内容（如：“消融实验数据对比表”）。
* **判定逻辑**：如果文件名包含 "table"，脚本会自动归类为 tables，否则归类为 figures。

### CSS 作用域与命名规范 (强制规则)

为了避免多页 PPT 合并时的 CSS 冲突，必须遵守以下规范：


#### 1. 视口适配与页面作用域
浏览器重置：必须设置 html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; } 以消除滚动条。

视口容器：整个 PPT 页面必须被 <div class="ppt-slide"> 包裹。该容器必须设为 width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; background: #333; 以确保画布在浏览器中居中且不溢出。

画布容器：#ppt-canvas 必须作为 .ppt-slide 的直接子元素。

---

#### 2. 所有 CSS 选择器必须带作用域前缀

所有 CSS 选择器必须以 `.ppt-slide` 作为前缀，防止全局样式污染。

正确示例：

```
.ppt-slide #ppt-canvas { }

.ppt-slide .ppt-title { }

.ppt-slide .text-block { }

.ppt-slide .layout-block { }

.ppt-slide .figure-container { }
```

---

#### 3. 严禁使用全局标签选择器

禁止直接使用以下写法：

```
header { }
main { }
img { }
p { }
section { }
ul { }
```

必须写成：

```
.ppt-slide header { }

.ppt-slide main { }

.ppt-slide img { }

.ppt-slide p { }
```

---

#### 4. 类名必须保持协议一致

以下类名 **严禁修改或替换**：

* `ppt-title`
* `ppt-authors`
* `header-logos`
* `layout-block`
* `section-header`
* `text-block`
* `list-item`
* `references-text`
* `figure-container`
* `row-container`
* `column`

---

#### 5. 允许新增类名，但必须遵守命名规范

新增类名必须使用 **kebab-case（短横线命名）**：

示例：

```
.sidebar-decoration
.content-area
.footer-info
.figure-wrapper
.text-highlight
```

禁止：

```
sidebarDecoration
SidebarDecoration
sidebar_decoration
```

---

#### 6. CSS 必须写在 `<style>` 中

HTML 必须为 **单文件结构**，所有样式必须写在 `<style>` 标签内。

---

### 布局精度要求

* **位置对齐**：严格参考 json 的 bbox 坐标，通过 flex / grid 确保元素顺序与物理位置对齐。
* **字体信息**：根据图片中的语义信息和尺寸信息识别不同文本的字体、大小、粗细和间距等信息，务必做到布局与图中所示相同。

---

### 禁令

* 严禁修改类名（Class Name），必须与上述协议完全一致。
* 严禁在 `layout-block` 内部使用不规范的嵌套（如在 `p` 标签外直接裸露文字）。
* 严禁生成任何全局 CSS 选择器（所有选择器必须带 `.ppt-slide` 前缀）。
* 严禁生成 Markdown 或解释文本。
* **必须直接输出以 `<!DOCTYPE html>` 开头的 HTML 代码字符串。**

---

### 正确结构示例

<header>
    <h1 class="ppt-title">论文标题</h1>
    <p class="ppt-authors">作者A, 作者B</p>
    <div class="header-logos">
        <div>XX 大学</div>
        <div>github.com/project</div>
        <img src="./slide_0_fig_1.jpg" style="width: 100px; height: 100px;" data-semantic="校徽">
    </div>
</header>

<main>
    <div class="column">
        <section class="layout-block" data-section-id="section_1">
            <h2 class="section-header">引言</h2>
            <p class="text-block">这是正文内容。</p>

            <div class="figure-container">
                <img src="./slide_3_fig_1.jpg" style="width: 500px; height: 300px;" data-semantic="模型架构图">
            </div>

        </section>
    </div>
</main>
"""
    final_prompt = prompt.replace("{{WIDTH}}", str(WIDTH)).replace("{{HEIGHT}}", str(HEIGHT))
    message=[
        {"role": "system", "content": """你是一个资深的前端布局工程师。你擅长使用现代 CSS Flexbox 技术复刻复杂的ppt布局。
你的代码风格要求：
1. 必须使用 Flexbox (display: flex) 处理多栏布局。
2. 严禁使用 <table>、<float> 或过度的 position: absolute。
3. 代码结构必须语义化，通过容器嵌套来表达层级逻辑。
4. 所有布局参数（gap, width, padding）必须参考视觉特征和 bbox 坐标。"""},

        {"role": "user", "content":[
            {"type":"text","text":prompt},
            {"type":"text","text":"我将给出ppt的图片形式，以及ppt中分割出来的图像和表格，请根据这些内容生成对应的HTML数据。"},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image_encode(ppt_image)}"
                }
            },
            *multimodal_content,
            {
                "type":"text",
                "text":"我将给出基于XML分析得到的版面布局信息的content_list.json结果，内容是基于XML解析的元素阅读顺序和各元素的bbox等信息，请你参考该json(特别是bbox这一位置信息)来辅助生成最终的html代码"
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
    img_path="../webData/imgs/AdaMML_ Adaptive Multi-Modal Learning for Efficient Video Recognition.png"
    poster_name=Path(img_path).stem
    print(poster_name)
    sub_image_path=f'../webData/mineru_output'
    ppt_path='../pptDataOutput/7ECNQNAGJJXYYTP7NJJZXFBPFEYRSNIZ'
    for index in range(8):

        html_code=singele_poster_process(ppt_path,index)
        print(html_code)
        html_path=f'./7ECNQNAGJJXYYTP7NJJZXFBPFEYRSNIZ_{index}.html'
        save_html(html_path,html_code)