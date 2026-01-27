import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from pathlib import Path
from utils.JsonTools import load_json
from openai import OpenAI
import base64
from PIL import Image
import json
from dotenv import load_dotenv

# 加载 .env 文件（必须在 getenv 之前执行）
load_dotenv() 
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
# 使用示例（1张或N张都适用）

def get_json_data(poster_path,poster_name,sub_image_path):#针对一个海报，调用llm获取json数据
    poster_path=poster_path/poster_name
    #print("poster_path:",poster_path)
    poster_base64=image_encode(poster_path)
    images_path=get_figures_path(sub_image_path,poster_name)
    tables_path=get_tables_path(sub_image_path,poster_name)
    #print("images_path:",images_path)
    #print("tables_path:",tables_path)
    image_contents=build_images_message(images_path,tables_path)
    multimodal_content=build_multimodal_prompt(image_contents)
    prompt="""
    你是一个专业的学术海报内容提取助手，能够从学术海报中提取对应的文本内容、图像和表格，并将其组织成结构化的JSON格式。请根据以下要求生成JSON数据：
    {

  "metadata":{

    "title":海报的标题（参考文档标题给出）

    "authors":按照海报中的顺序给出所有的作者

    "github":如果海报中提供了相关的GitHub连接，则填入本字段，否则留空，例如"github":""。

    "description":对海报内容的简短描述

  }

  "sections": [

    {

      "id": "section1",

      "title": section标题,

      "content": ["",""],content部分以一个list给出，list的每个元素是一段正文文本，不同元素表示不同分段

      "tables": [],

      "figures": []

    },

    {

      "id": "section2",

      "title": "",

      "content": ["",""],

      "tables": [],

      "figures": [{"fig_id": "fig_2","figure_weight":"","figure_height":""}]

    },

    {

      "id": "section3",

      "title": "",

      "content": ["",""],

      "tables": [{"table_id": "table_1","table_weight":"","table_height":""}],

      "figures": []

    }

  ]

}

请注意以下几点：
1. JSON结构必须严格遵循上述格式，包括metadata和sections字段。
2. metadata部分包含海报的基本信息，如标题、作者、GitHub链接和描述。
3. sections部分是一个数组，每个元素代表海报的一个章节。每个章节包含标题、正文内容、图像和表格。
4. content字段是一个列表，列表中的每个元素是一段正文文本，你必须精准的提取文本内容，不能对原图的信息进行修改或省略等。
5. figures和tables字段分别包含文件名和尺寸信息。我会给出图像和表格的文件名、尺寸信息以及分割出来的图表，你需要将这些文件名与海报中的实际内容对应起来，并填写尺寸信息，单位为px。
6. 只输出要求的结构化json数据，不要输出任何多余的字符

"""

    messages=[
        {"role": "system", "content": "你是一个专业的学术海报内容提取助手，能够从学术海报中提取对应的文本内容、图像和表格，并将其组织成结构化的JSON格式。"},
        {"role": "user", "content":[
            {"type":"text","text":prompt},
            {"type":"text","text":"我将给出海报的图片，以及海报中分割出来的图像和表格，请根据这些内容生成对应的JSON数据。"},
            {
                "type":"image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{image_encode(poster_path)}"
                }
            },
            *multimodal_content
            ]
        },
    ]
    #print(multimodal_content)
    with open('./test.json','w',encoding='utf-8') as f:
        json.dump(messages,f,ensure_ascii=False,indent=2)
    api=os.getenv("API_KEY")
    url=os.getenv("BASE_URL")
    model_name=os.getenv("VISUAL_MODEL","qwen3-max")
    #print(f"api:{api}")
    client=OpenAI(
        api_key=api,
        base_url=url
    )
    response=client.chat.completions.create(
        model=model_name,  # 或任意你想试的 Gemini 模型
        messages=messages,
        temperature=0
    )
    #print(response.choices[0].message.content)
    return response.choices[0].message.content

def get_json_data_batch(poster_path,sub_image_path,save_path):
    poster_path=Path(poster_path)
    for item in poster_path.iterdir():
        if item.suffix=='.jpg':
            poster_name=item
            json_data=get_json_data(poster_path,poster_name,sub_image_path)
            poster_name_with_no_suffix=poster_name[:-4]
            save_file=save_path/f"{poster_name_with_no_suffix}.json"
            save_file.parent.mkdir(parents=True,exist_ok=True)
            with open(save_file,'w',encoding='utf-8') as f:
                json.dump(json_data,f,ensure_ascii=False,indent=2)

if __name__ == "__main__":
    poster_path=Path("../posterData")
    #poster_name="[Re] Graph Edit Networks_poster.jpg"
    sub_image_path=Path("../posterDataOutput")
    #get_json_data(poster_path,poster_name,sub_image_path)
    get_json_data_batch(poster_path,sub_image_path,save_path=sub_image_path)