# 1. 安装依赖（仅需一次）
# pip install openai
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from pathlib import Path
from utils.JsonTools import load_json,save_json
from openai import OpenAI
import base64
from PIL import Image 
def image_encode(img_path):
        with open(img_path, "rb") as f:
            img_data = f.read()
        encoded_str = base64.b64encode(img_data).decode("utf-8")
        return encoded_str

def get_image_size(path):
    w, h = Image.open(path).size
    return w,h


def get_figures_path(output_dir, file_name):#获取海报中所有图片的路径
    file_name=file_name[:-4]
    image_dict_path=Path(output_dir)/file_name/"dict"/"images.json"
    images_path=[]
    image_dict=load_json(image_dict_path)
    for img in image_dict:
        images_path.append([img["fig_id"],img["path"]])
    return images_path

def get_tables_path(output_dir, file_name):#获取海报中所有表格的路径
    file_name=file_name[:-4]
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

    poster_file=poster_path/poster_name

    images_path=get_figures_path(sub_image_path,poster_name)
    tables_path=get_tables_path(sub_image_path,poster_name)

    image_contents=build_images_message(images_path,tables_path)
    multimodal_content=build_multimodal_prompt(image_contents)

    prompt="""
我将给出原始海报的图片和海报中的子图(包括图片和表格)以及这些图片对应的尺寸信息，请根据这些信息输出能表达海报布局信息的html代码
请注意以下几点：
1. 最终通过html生成的海报尺寸要与海报图片的尺寸保持一致
2. 最终通过html生成的海报中的子图(包括图片和表格)尺寸要与我给出的子图尺寸保持一致，在html中通过相对路径的形式表示子图，例如'./fig_1.jpg'。如果海报中存在我没有给出的子图，则请你根据海报原图和其他子图的信息判断该图片的尺寸信息，在html表示中用一个矩形占位框表示，并附加相关的语义信息来表示图片。
3. 对于海报中的标题、文本和公式等文本信息，你要严格遵循原图中的信息进行提取，不得对文本信息做修改、删减或增加等操作。
4. 对于文本信息的换行、字体大小和行间距等影响布局的因素，你要严格遵循原始海报中的设置，保证通过html表示的海报中的一段文本和原图中对应的文本所占的面积相等。
5. 你的核心任务是一比一复刻原图的布局信息，不得做任何修改和优化。例如原图中两张图是横向排列，那么html中就必须是横向排列。
6. 对于图片和表格的caption，你要一字不差的提取其文本信息，并遵循原图保持和图片的相对位置。
7. 不要遗漏任何文本、公式、图片或表格信息
8. 你的任务是识别并复现学术海报的布局信息，不需要生成任何style相关的信息，例如颜色等。但字体等影响布局的信息必须判断并生成。
9. 你只需要生成可以直接在浏览器中展示的html代码，不要输出任何多余的字符。
"""
    message=[
        {"role": "system", "content": "你是一个专业的学术海报布局信息提取助手，能够精准的识别学术海报的布局信息，并输出一端html代码来一比一的复现原图中的布局"},
        {"role": "user", "content":[
            {"type":"text","text":prompt},
            {"type":"text","text":"我将给出海报的图片，以及海报中分割出来的图像和表格，请根据这些内容生成对应的JSON数据。"},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image_encode(poster_file)}"
                }
            },
            *multimodal_content
            ]
        }
    ]
    api=os.getenv("API_KEY")
    url=os.getenv("BASE_URL")
    model_name=os.getenv("VISUAL_MODEL","qwen3-max")
    client=OpenAI(
        api_key=api,
        base_url=url
    )
    resp = client.chat.completions.create(
        model="liquid/lfm-2.5-1.2b-thinking:free",  # 或任意你想试的 Gemini 模型
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
    img_path="../posterData/[Re] Graph Edit Networks_poster.jpg"
    html_code=singele_poster_process(img_path)
    print(html_code)