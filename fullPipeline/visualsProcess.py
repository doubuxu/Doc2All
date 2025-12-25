import base64
from pathlib import Path
from openai import OpenAI
from PIL import Image
from utils.JsonTools import save_json,load_json
def getCaption(image_path:str,object:str):
    client=OpenAI(
        api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    if object=="image":
        message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "You are a detail-oriented image describer.Given the input image, write ONE concise yet complete caption for the image.Another LLM must understand the image through your caption"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64}"   # 关键行
                    }
                }
            ]
        }
        ]
    elif object=="table":
        message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "You are a detail-oriented table describer.Given the input table, write ONE concise yet complete caption for the table.Another LLM must understand the table through your caption"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64}"   # 关键行
                    }
                }
            ]
        }
        ]     
    caption=client.chat.completions.create(
        model="qwen3-vl-8b-instruct",
        messages=message,
        temperature=0
    )
    return caption.choices[0].message.content

def get_image_size(path):
    w, h = Image.open(path).size
    return w,h

def postProcessImages(output_path,file_name):#输入路径和文件名，为图片和表格dict添加llm_description字段和尺寸字段
    image_dict_path=Path(output_path)/file_name/"dict"/"images.json"
    table_dict_path=Path(output_path)/file_name/"dict"/"tables.json"
    image_dict=load_json(image_dict_path)
    table_dict=load_json(table_dict_path)
    
    for index,img in enumerate(image_dict):
        description=getCaption(img["path"],"image")
        img["llm_description"]=description
        w,h=get_image_size(img["path"])
        img["weight"]=w
        img["height"]=h
    save_json(image_dict,image_dict_path)
    
    for index,table in enumerate(table_dict):
        print(index)
        print(table["path"])
        description=getCaption(table["path"],"table")
        table["llm_description"]=description
        w,h=get_image_size(table["path"])
        table["weight"]=w
        table["height"]=h
    save_json(table_dict,table_dict_path)

def insertDictInMD(output_dir,file_name):
    md_path=Path(output_dir)/file_name/f'{file_name}.md'
    image_dict_path=Path(output_dir)/file_name/"dict"/"images.json"
    table_dict_path=Path(output_dir)/file_name/"dict"/"tables.json"
    md_content=Path(md_path).read_text(encoding='utf-8')
    images_dict=load_json(image_dict_path)
    tables_dict=load_json(table_dict_path)

    for index,img in enumerate(images_dict):
        img_path=img["img_path"]
        img_path=img_path[1:-1]
        #在md_content中找到img_path对应的位置，插入描述
        md_content=md_content.replace(img_path,img)

    for index,table in enumerate(tables_dict):
        table_body=table["table_body"]
        table_body=table_body[1:-1]
        #在dict中table是一行，在md中是多行，要考虑换行符对字符串匹配的影响
        md_content=md_content.replace(table_body,table)

    with open(md_path,'w',encoding='utf-8') as f:
        f.write(md_content)  
    

if __name__=="__main__":
    postProcessImages("../data/output_general","docsam")
