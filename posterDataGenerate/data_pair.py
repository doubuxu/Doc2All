import os
from pathlib import Path
import sys
import json
from mineru_batch import mineru_process
from contentlistTojson import transform
from htmlDataGenerate import singele_poster_process
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import load_json,save_json
from utils.htmlTools import save_html
def single_poster_data_generate(poster_pdf_path,poster_img_path,output_dir):
    """
    输入海报的pdf路径让mineru处理，指定输出路径，得到content_list.json文件和分割后的子图
    读取content_list.json的数据，经过transform返回content_plan.json
    根据poster_path路径读取海报png路径，结合content_plan.json和分割后的子图，生成html代码
    """
    mineru_process(poster_pdf_path,output_dir)
    poster_name=Path(poster_pdf_path).stem
    content_list_path=Path(output_dir)/poster_name/f"{poster_name}_content_list.json"
    content_list=load_json(content_list_path)
    content_plan=transform(content_list)
    html_code=singele_poster_process(poster_img_path,poster_name,output_dir)
    return content_plan,html_code

def batch_poster_data_generate(poster_pdf_dir,poster_img_dir,pair_data_dir,output_dir):
    poster_pdf_dir=Path(poster_pdf_dir)
    for item in poster_pdf_dir.iterdir():
        poster_pdf_path=item
        if poster_pdf_path.suffix.lower() not in ['.pdf']:
            continue
        poster_name=Path(poster_pdf_path).stem
        poster_img_path=Path(poster_img_dir)/f"{poster_name}.jpg"
        content_plan,html_code=single_poster_data_generate(poster_pdf_path,poster_img_path,output_dir)
        html_code = html_code[7:-3]
        save_json(content_plan,Path(pair_data_dir)/"json_data"/f"{poster_name}_content_plan.json")
        save_html(Path(pair_data_dir)/"html_data"/f"{poster_name}.html",html_code)
        #break # 目前只处理一个文件，后续再批量处理 

if __name__=="__main__":
    poster_pdf_dir="../posterData"
    poster_img_dir="../posterData"
    pair_data_dir="../poster_pair_data"
    output_dir="./output"

    batch_poster_data_generate(poster_pdf_dir,poster_img_dir,pair_data_dir,output_dir)
    #content_plan, html_code = single_poster_data_generate("../posterData/[Re] Graph Edit Networks_poster.pdf","../posterData/[Re] Graph Edit Networks_poster.jpg","./output")
    #html_code = html_code[7:-3]
    #poster_name = "[Re] Graph Edit Networks_poster"
    #save_json(content_plan,Path(pair_data_dir)/"json_data"/f"{poster_name}_content_plan.json")
    #save_html(Path(pair_data_dir)/"html_data"/f"{poster_name}.html",html_code)