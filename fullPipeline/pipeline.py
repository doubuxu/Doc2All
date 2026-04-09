# -*- coding: utf-8 -*-
import argparse
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from pathlib import Path
import shutil 
from parse import parse_doc
from contentPlan import content_plan,content_plan_with_check
from jinja2 import Environment
from jinja2 import Template
import json
from visualsProcess import getCaption,postProcessImages,insertDictInMD
from utils.JsonTools import load_json,save_json
from htmlGenerate import htmlCodeWithbase64
from utils.htmlTools import load_html,save_html
from logger import get_logger
import dotenv
import time
import datetime
from utils.token_claculate import token_sum
from utils.logo_fetch import LogoFetcher
from utils.download_logo import download_logo_simple
import requests
from urllib.parse import urlparse
from htmlGenerateLocal import htmlGenerate,htmlGenerateBaseline
from posterDataGenerate.mineru_batch import mineru_process
from changeHTMLPath import changeHTML
from replaceTableImages import replace_table_images_with_html
from metadata_enrich import enrich_content_plan_metadata
dotenv.load_dotenv()
#pdf_path=""
#parse_doc()

def get_logo_by_domain(institution_name):
    """通过机构域名获取Logo"""
    # 需要先获取机构的官方域名
    # 可通过OpenAlex的institution API获取homepage_url
    
    # 示例：MIT -> mit.edu
    domain = "mit.edu"  # 从OpenAlex获取
    logo_url = f"https://logo.clearbit.com/{domain}"
    return logo_url

def args_analyse():
    parser = argparse.ArgumentParser(description='input args')
    parser.add_argument('--doc_path', help='input Document path')
    parser.add_argument('-o', '--output', default='output', help='output path')
    parser.add_argument('--mode',required=True,choices=['ppt','poster','web'],help='choose the final output')
    parser.add_argument('--github_url', default='', help='optional GitHub URL to override metadata.github')
    parser.add_argument('--arxiv_url', default='', help='optional arXiv URL to override metadata.arxiv_id')
    #parser.add_argument('--overwrite', action='store_true', help='���������ļ�')
    args = parser.parse_args()
    return args


def ppt_generate(input_path,output_path):#baselineModel1
    input_path=Path(arg.doc_path).resolve()
    output_path=Path(arg.output).resolve()
    file_name=input_path.stem
    parse_doc(input_path,output_path)

    postProcessImages(output_path,file_name)

    md_path=Path(output_path)/file_name/f'{file_name}.md'
    image_dict_path=Path(output_path)/file_name/"dict"/"images.json"
    table_dict_path=Path(output_path)/file_name/"dict"/"tables.json"

    #content_plan�׶�
    content_plan_prompt_template=Template(open('prompts/content_plan.txt').read())
    markdown_content=Path(md_path).read_text(encoding='utf-8')
    images_dict=load_json(image_dict_path)
    table_dict=load_json(table_dict_path)
    content_plan_prompt=content_plan_prompt_template.render(document=markdown_content,images=images_dict,tables=table_dict)
    content_plan_json_path=Path(output_path)/file_name/f"{file_name}_content_plan.json"
    contentPlan=content_plan(content_plan_prompt,content_plan_json_path)

    #generate�׶�
    html_generate_prompt_template=Template(open('prompts/htmlGenerate.txt').read())
    html_generate_prompt=html_generate_prompt_template.render(contentplan=contentPlan)
    html_code=htmlCodeWithbase64(html_generate_prompt,output_path,file_name)
    html_path=Path(output_path)/file_name/f"{file_name}.html"
    save_html(html_path,html_code)

def ppt_generate2(input_path,output_path,mode,log,github_url="",arxiv_url=""):#baselineModel2
    input_path=Path(arg.doc_path).resolve()
    output_path=Path(arg.output).resolve()
    file_name=input_path.stem
    log.info("Start document parsing...")
    parse_doc(input_path,output_path)
    log.info("Document parsing completed.")

    log.info("start planing slides content...")
    content_plan=content_plan_with_check(output_path,file_name,"",max_try=1,mode=mode,log=log)
    content_plan = enrich_content_plan_metadata(
        content_plan,
        output_path,
        file_name,
        log=log,
        github_url=github_url,
        arxiv_url=arxiv_url,
    )

    log.info("Slides content planning completed.")
    log.info("Start html code generation...")
    if mode=="ppt":
        html_generate_prompt_template=Template(open('prompts/ppt_htmlGeneratev2.txt').read())
    elif mode=="poster":
        html_generate_prompt_template=Template(open('prompts/poster_htmlGenerate.txt').read())
    elif mode=="web":
        html_generate_prompt_template=Template(open('prompts/web_htmlGenerate.txt').read())
    html_generate_prompt=html_generate_prompt_template.render(contentplan=content_plan)
    #print(html_generate_prompt)
    html_code=htmlCodeWithbase64(html_generate_prompt,output_path,file_name,mode,log)
    html_path=Path(output_path)/file_name/"htmlGenerate"/f"{file_name}.html"
    save_html(html_path,html_code)
    log.info("Html code generation completed.")
    token_sum(output_path,file_name)


def presentation_generate(input_path,output_path,mode,log,github_url="",arxiv_url=""):
    #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #input_path=Path(arg.doc_path).resolve()
    #output_path=Path(arg.output).resolve()
    file_name=Path(input_path).stem
    log.info("Start document parsing...")
    #parse_doc(input_path,output_path)
    mineru_process(input_path,output_path)
    postProcessImages(output_path,file_name)
    insertDictInMD(output_path,file_name)
    log.info("Document parsing completed.")

    log.info("start planing slides content...")
    content_plan=content_plan_with_check(output_path,file_name,"",max_try=1,mode=mode,log=log)
    content_plan = enrich_content_plan_metadata(
        content_plan,
        output_path,
        file_name,
        log=log,
        github_url=github_url,
        arxiv_url=arxiv_url,
    )
    log.info("Slides content planning completed.")
    log.info("Start html code generation...")
    html_code = htmlGenerate(content_plan,data_type=mode)
    #html_code = htmlGenerateBaseline(content_plan,data_type=mode)
    html_code = changeHTML(html_code)#修改图片引用路径
    if mode == "web":
        html_code = replace_table_images_with_html(
            html_code,
            Path(output_path) / file_name,
            log=log,
        )
    save_html(Path(output_path)/file_name/f"{file_name}.html",html_code)

    log.info("html code generation finished")
    token_sum(output_path,file_name)
    #new_path=output_path/f"{timestamp}_{file_name}_{mode}"
    #shutil.move(output_path/file_name,new_path)


if __name__=="__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #输入参数指定output，在output下结构存储md等文件
    arg=args_analyse()
    input_path=Path(arg.doc_path).resolve()
    output_path=Path(arg.output).resolve()
    mode=arg.mode
    github_url=arg.github_url
    arxiv_url=arg.arxiv_url
    file_name=input_path.stem
    log = get_logger(output_path,file_name,__name__)
    log.info(f"Processing document: {input_path}, output to: {output_path},file_name: {file_name}")
    #ppt_generate2(input_path,output_path,mode=mode,log=log)
    presentation_generate(
        input_path,
        output_path,
        mode,
        log,
        github_url=github_url,
        arxiv_url=arxiv_url,
    )
    new_path=output_path/f"{timestamp}_{file_name}_{mode}"
    shutil.move(output_path/file_name,new_path)
    """
    #基于mineru做pdf文档解析，解析结果保存到output_path
    parse_doc(input_path,output_path)

    #content plan�׶�
    #��ȡmd�ļ���·��
    md_path=Path(output_path)/file_name/f'{file_name}.md'
    image_dict_path=Path(output_path)/file_name/"dict"/"images.json"
    table_dict_path=Path(output_path)/file_name/"dict"/"tables.json"
    #print(md_path)
    
    
    with open(image_dict_path,'r',encoding='utf-8') as f:
        image_dict=json.load(f)
    for index,img in enumerate(image_dict):
        description=getCaption(img["path"])
        img["llm_description"]=description

    with open(image_dict_path,'w',encoding='utf-8') as f:
        json.dump(image_dict,f,ensure_ascii=False,indent=2)        
    
    postProcessImages(output_path,file_name)


    prompt_template=Template(open('prompts/content_plan.txt').read())
    markdown_content=Path(md_path).read_text(encoding='utf-8')
    images_dict=load_json(image_dict_path)
    table_dict=load_json(table_dict_path)
    prompt=prompt_template.render(document=markdown_content,images=images_dict,tables=table_dict)
    content_plan_json=Path(output_path)/file_name/f"{file_name}_content_plan.json"
    contentPlan=content_plan(prompt,content_plan_json)
    """

    
