from openai import OpenAI
from pathlib import Path
from utils.JsonTools import load_json,save_json
from utils.imgEncode import imgEncoder
from jinja2 import Template
import re, json, base64, pathlib
def save_html(save_path:str,code:str):
    with open(save_path,'w',encoding='utf-8') as f:
        f.write(code)

def load_html(html_path):
    with open(html_path,'r',encoding='utf-8') as f:
        data=f.read()
    return data


def htmlCodeGenerate(prompt:str) -> str:
    client = OpenAI(
    api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
    )

    #test=Template(open('prompts/paper_content_plan.txt').read())

    response = client.chat.completions.create(
        model="qwen3-max",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        temperature=0,
        extra_body={"enable_thinking": False}
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def find_block(html_code:str)->str:#查找html代码中的pptData 区块
    m = re.search(r'(const\s+pptData\s*=\s*)(\{.*?\})\s*;', html_code, flags=re.S)
    if not m:
        raise RuntimeError('找不到 pptData 区块')
    prefix, json_block = m.groups()
    data = json.loads(json_block)
    return data

def generate_id_to_basecode(output_path:str,file_name:str):#生成fig_id到base64编码的映射
    id_to_code_map={}
    image_dict_path=Path(output_path)/file_name/"dict"/"images.json"
    image_dict=load_json(image_dict_path)
    for index,image in enumerate(image_dict):
        fig_id=image["fig_id"]
        base64_code=imgEncoder(image["path"])
        id_to_code_map[fig_id]=base64_code
    return id_to_code_map

def add_base64_code(pptData:str,id_to_code_map):
    for index,slide in enumerate(pptData["slides"]):
        figures=slide["figures"]
        #figures_num=len(figures)
        for i in range(len(figures)):
            figure=figures[i]
            figure_id=figure["fig_id"]
            base64_code=id_to_code_map[figure_id]
            figure["base64_code"]=base64_code
    save_json(pptData,'./codeTest.json')
    

if __name__=="__main__":
    """
    content_plan=load_json('../data/output/docsam/docsam_content_plan.json')
    prompt_template=Template(open('./prompts/htmlGenerate.txt').read())
    prompt=prompt_template.render(contentplan=content_plan)
    html_code=htmlCodeGenerate(prompt)
    save_html('../data/output/docsam/final.html',html_code)
    """
    html_code=load_html('../data/output/docsam/final.html')
    pptData=find_block(html_code)
    map_a=generate_id_to_basecode('../data/output','docsam')
    save_json(map_a,'./test.json')
    add_base64_code(pptData,map_a)
