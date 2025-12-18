# -*- coding: utf-8 -*-
import argparse
import os
from pathlib import Path 
from parse import parse_doc
from contentPlan import content_plan
from jinja2 import Environment
from jinja2 import Template
import json
from generateCaption import getCaption,postProcessImages
from utils.JsonTools import load_json,save_json
#pdf_path=""
#parse_doc()

def args_analyse():
    parser = argparse.ArgumentParser(description='input args')
    parser.add_argument('--doc_path', help='input Document path')
    parser.add_argument('-o', '--output', default='output', help='output path')
    #parser.add_argument('--overwrite', action='store_true', help='覆盖已有文件')
    args = parser.parse_args()
    return args


if __name__=="__main__":

    #输入参数指定output，在output下结构存储md等文件
    arg=args_analyse()
    input_path=Path(arg.doc_path).resolve()
    output_path=Path(arg.output).resolve()
    file_name=input_path.stem
    #基于mineru做pdf文档解析，解析结果保存到output_path
    parse_doc(input_path,output_path)

    #content plan阶段
    #获取md文件的路径
    md_path=Path(output_path)/file_name/f'{file_name}.md'
    image_dict_path=Path(output_path)/file_name/"dict"/"images.json"
    table_dict_path=Path(output_path)/file_name/"dict"/"tables.json"
    #print(md_path)
    
    """
    with open(image_dict_path,'r',encoding='utf-8') as f:
        image_dict=json.load(f)
    for index,img in enumerate(image_dict):
        description=getCaption(img["path"])
        img["llm_description"]=description

    with open(image_dict_path,'w',encoding='utf-8') as f:
        json.dump(image_dict,f,ensure_ascii=False,indent=2)        
    """
    postProcessImages(output_path,file_name)


    #加载prompt
    #prompt_template=Template(open('prompts/paper_content_plan.txt').read())
    prompt_template=Template(open('prompts/content_plan.txt').read())
    markdown_content=Path(md_path).read_text(encoding='utf-8')
    images_dict=load_json(image_dict_path)
    table_dict=load_json(table_dict_path)
    prompt=prompt_template.render(document=markdown_content,images=images_dict,tables=table_dict)
    content_plan_json=Path(output_path)/file_name/f"{file_name}_content_plan.json"
    content_plan(prompt,content_plan_json)
    
    


