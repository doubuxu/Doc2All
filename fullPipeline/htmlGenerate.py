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
    return pptData

def replace_pptData_block(html_code: str, new_pptData: dict) -> str:
    """
    用 new_pptData 重新生成美化后的 JSON，替换原 HTML 中的 pptData 区块。
    返回完整的新 HTML 字符串。
    """
    # 1. 美化序列化（ensure_ascii=False 保证中文不转义）
    new_json_str = json.dumps(new_pptData, ensure_ascii=False, indent=2)

    # 2. 正则定位原区块
    pattern = re.compile(r'(const\s+pptData\s*=\s*)(\{.*?\})\s*;', re.S)
    match = pattern.search(html_code)
    if not match:
        raise RuntimeError('找不到 pptData 区块，无法替换')

    # 3. 拼接新内容（保留原来的 const pptData =  和  分号）
    replaced_html = (
        html_code[:match.start(1)]        # const pptData = 之前的部分
        + match.group(1)                  # "const pptData = " 本身
        + new_json_str                    # 新的 JSON 美化串
        + ';'                             # 原来的分号
        + html_code[match.end():]         # 分号之后的所有 HTML
    )
    return replaced_html

def htmlCodeWithbase64(prompt:str,output_path,file_name):
    htmlCode=htmlCodeGenerate(prompt)
    pptData=find_block(htmlCode)
    id_map=generate_id_to_basecode(output_path,file_name)
    pptDataWithCode=add_base64_code(pptData,id_map)
    html_codeWithbase64=replace_pptData_block(htmlCode,pptDataWithCode)
    return html_codeWithbase64


if __name__=="__main__":
    """
    content_plan=load_json('../data/output/docsam/docsam_content_plan.json')
    prompt_template=Template(open('./prompts/htmlGenerate.txt').read())
    prompt=prompt_template.render(contentplan=content_plan)
    html_code=htmlCodeGenerate(prompt)
    save_html('../data/output/docsam/final.html',html_code)
    """
    """
    html_code=load_html('../data/output/docsam/final.html')
    pptData=find_block(html_code)
    map_a=generate_id_to_basecode('../data/output','docsam')
    save_json(map_a,'./test.json')
    add_base64_code(pptData,map_a)
    """
    content_plan=load_json('../data/output/docsam/docsam_content_plan.json')
    prompt_template=Template(open('./prompts/htmlGenerate.txt').read())
    prompt=prompt_template.render(contentplan=content_plan)
    htmlcode=htmlCodeWithbase64(prompt,'../data/output','docsam')
    save_html('./finalHtml.html',htmlcode)
