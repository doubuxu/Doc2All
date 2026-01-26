# -*- coding: utf-8 -*-
# Copyright (c) Opendatalab. All rights reserved.
import copy
import json
import os
from pathlib import Path
import pathlib
import shutil
from loguru import logger


from mineru.cli.common import convert_pdf_bytes_to_bytes_by_pypdfium2, prepare_env, read_fn
from mineru.data.data_reader_writer import FileBasedDataWriter
from mineru.utils.draw_bbox import draw_layout_bbox, draw_span_bbox
from mineru.utils.enum_class import MakeMode
from mineru.backend.vlm.vlm_analyze import doc_analyze as vlm_doc_analyze
from mineru.backend.pipeline.pipeline_analyze import doc_analyze as pipeline_doc_analyze
from mineru.backend.pipeline.pipeline_middle_json_mkcontent import union_make as pipeline_union_make
from mineru.backend.pipeline.model_json_to_middle_json import result_to_middle_json as pipeline_result_to_middle_json
from mineru.backend.vlm.vlm_middle_json_mkcontent import union_make as vlm_union_make
from mineru.utils.guess_suffix_or_lang import guess_suffix_by_path
#from visualsProcess import postProcessImages,insertDictInMD

def do_parse(
    output_dir:str,  # Output directory for storing parsing results
    input_file_name:str,  # List of PDF file names to be parsed
    pdf_bytes: bytes,  # List of PDF bytes to be parsed
    p_lang: str,  # List of languages for each PDF, default is 'ch' (Chinese)
    backend="pipeline",  # The backend for parsing PDF, default is 'pipeline'
    parse_method="auto",  # The method for parsing PDF, default is 'auto'
    formula_enable=True,  # Enable formula parsing
    table_enable=True,
    server_url=None,  # Server URL for vlm-http-client backend,����vlm
    f_draw_layout_bbox=True,  # Whether to draw layout bounding boxes
    f_draw_span_bbox=True,  # Whether to draw span bounding boxes
    f_dump_md=True,  # Whether to dump markdown files
    f_dump_middle_json=True,  # Whether to dump middle JSON files
    f_dump_model_output=True,  # Whether to dump model output files
    f_dump_orig_pdf=True,  # Whether to dump original PDF files
    f_dump_content_list=True,  # Whether to dump content list files
    f_make_md_mode=MakeMode.MM_MD,  # The mode for making markdown content, default is MM_MD
    start_page_id=0,  # Start page ID for parsing, default is 0
    end_page_id=None,  # End page ID for parsing, default is None (parse all pages until the end of the document)
):

    if backend == "pipeline":
        '''        
        for idx, pdf_bytes in enumerate(pdf_bytes_list):#����һ�����ַ����ʽת��
            new_pdf_bytes = convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
            pdf_bytes_list[idx] = new_pdf_bytes
        '''
        #处理pdf字节码
        pdf_bytes_tmp=convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
        pdf_bytes=pdf_bytes_tmp
        #step1

        #给定的接口是一次处理多个，所以改为list
        pdf_bytes=[pdf_bytes]
        p_lang=[p_lang]

        infer_results, all_image_lists, all_pdf_docs, lang_list, ocr_enabled_list = pipeline_doc_analyze(pdf_bytes, p_lang, parse_method=parse_method, formula_enable=formula_enable,table_enable=table_enable)
        

        for idx, model_list in enumerate(infer_results):
            model_json = copy.deepcopy(model_list)
            pdf_file_name = input_file_name
            local_image_dir, local_md_dir = prepare_env(output_dir, pdf_file_name, parse_method)#设置输出的md和图片路径
            #local_md_dir:outpout_dir/filename
            #local_image_dir:outpout_dir/filename/images

            image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)#写文件的类包装
            
            #images_writer=FileBasedDataWriter(str(images_dir))
            #tables_writer=FileBasedDataWriter(str(tables_dir))
            #equations_writer=FileBasedDataWriter(str(equations_dir))
            images_list = all_image_lists[idx]
            pdf_doc = all_pdf_docs[idx]
            _lang = lang_list[idx]
            _ocr_enable = ocr_enabled_list[idx]

            #标准中间输出
            middle_json = pipeline_result_to_middle_json(model_list, images_list, pdf_doc, image_writer,image_writer,image_writer,image_writer ,_lang, _ocr_enable, formula_enable)

            pdf_info = middle_json["pdf_info"]

            
            #写入md文件
            image_dir_abs=os.path.abspath(local_image_dir)
            make_func = pipeline_union_make
            md_content_str = make_func(pdf_info, f_make_md_mode, image_dir_abs)
            md_writer.write_string(
                f"{pdf_file_name}.md",
                md_content_str,
            )
            #print(f"md_content_str:{md_content_str}")

            
            #准备写入content_list内容
            #content_list中的visuals的路径是local_image_dir与相对路径的拼接
            make_func = pipeline_union_make 
            content_list = make_func(pdf_info, MakeMode.CONTENT_LIST,image_dir_abs)
            
            images_list=[]
            tables_list=[]
            equations_list=[]
            images_name=[]
            tables_name=[]
            eqs_name=[]
            fig_index=1
            table_index=1
            eq_index=1
            for index,entity in enumerate(content_list):
                if entity["type"]=="image":
                    image_info={
                        "fig_id":f"fig_{fig_index}",
                        "path": entity["img_path"],
                        "caption":entity["image_caption"],
                        "content_list_index":index
                    }
                    images_name.append(Path(entity["img_path"]).name)
                    images_list.append(image_info)
                    fig_index+=1
                elif entity["type"]=="table" :
                    if entity["img_path"] !="" and "table_body" in entity:
                        table_info={
                            "table_id":f"table_{table_index}",
                            "path":entity["img_path"],
                            "caption":entity["table_caption"],
                            "content_list_index":index,
                            "table_body":entity["table_body"]
                        }
                        tables_name.append(Path(entity["img_path"]).name)
                        tables_list.append(table_info)
                        table_index+=1
                elif entity["type"]=="equation":
                    equations_info={
                        "equations_id":f"equations_{eq_index}",
                        "path":entity["img_path"],
                        "content_list_index":index
                    }
                    eqs_name.append(Path(entity["img_path"]).name)
                    equations_list.append(equations_info)
                    eq_index+=1
            
            

            images_dir=Path(image_dir_abs)/"images"
            tables_dir=Path(image_dir_abs)/"tables"
            equations_dir=Path(image_dir_abs)/"equations"
            os.makedirs(images_dir,exist_ok=True)
            os.makedirs(tables_dir,exist_ok=True)
            os.makedirs(equations_dir,exist_ok=True)
            for file in Path(local_image_dir).iterdir():
                #file是包含完整路径的
                file=file.resolve()
                name=Path(file).name
                #print(f"path:{file}")
                #print("name")
                #print(name)
                if name in images_name:
                    index=images_name.index(name)
                    new_name=images_list[index]["fig_id"]+".jpg"
                    
                    dst=images_dir/new_name
                    #print(f"new_path:{dst}")
                    shutil.move(str(file),str(dst))
                    images_list[index]["path"]=str(dst)
                    content_list_index=images_list[index]["content_list_index"]
                    content_list[content_list_index]["img_path"]=str(dst)#替换content_list中的图片路径
                    md_content_str=md_content_str.replace(str(file),str(dst))
                elif name in tables_name:
                    index=tables_name.index(name)
                    new_name=tables_list[index]["table_id"]+".jpg"
                    
                    dst=tables_dir/new_name
                    #print(f"new_path:{dst}")
                    shutil.move(str(file),str(dst))
                    tables_list[index]["path"]=str(dst)
                    content_list_index=tables_list[index]["content_list_index"]
                    content_list[content_list_index]["img_path"]=str(dst)
                    md_content_str=md_content_str.replace(str(file),str(dst))
                elif name in eqs_name:
                    index=eqs_name.index(name)
                    new_name=equations_list[index]["equations_id"]+".jpg"
                    
                    dst=equations_dir/new_name
                    #print(f"new_path:{dst}")
                    shutil.move(str(file),str(dst))
                    equations_list[index]["path"]=str(dst)
                    content_list_index=equations_list[index]["content_list_index"]
                    content_list[content_list_index]["img_path"]=str(dst)
                    md_content_str=md_content_str.replace(str(file),str(dst))

            dict_path=Path(local_md_dir)/"dict"
            os.makedirs(dict_path, exist_ok=True)
            with open(dict_path/"images.json",'w',encoding='utf-8') as f:
                    json.dump(images_list,f,ensure_ascii=False, indent=2)
            
            with open(dict_path/"tables.json",'w',encoding='utf-8') as f:
                    json.dump(tables_list,f,ensure_ascii=False, indent=2)

            with open(dict_path/"equations.json",'w',encoding='utf-8') as f:
                    json.dump(equations_list,f,ensure_ascii=False, indent=2)
            md_writer.write_string(
                f"{pdf_file_name}_content_list.json",
                json.dumps(content_list, ensure_ascii=False, indent=4),
            )  
            md_writer.write_string(
                f"{pdf_file_name}.md",
                md_content_str,
            )
            pdf_bytes=pdf_bytes[0]
            draw_layout_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_layout.pdf")
            draw_span_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_span.pdf")
            '''
            _process_output(
                pdf_info, pdf_bytes, pdf_file_name, local_md_dir, local_image_dir,
                md_writer, f_draw_layout_bbox, f_draw_span_bbox, f_dump_orig_pdf,
                f_dump_md, f_dump_content_list, f_dump_middle_json, f_dump_model_output,
                f_make_md_mode, middle_json, model_json, is_pipeline=True
            )
            '''

    #backend
    

    else:#暂时不考虑这个分支
        if backend.startswith("vlm-"):
            backend = backend[4:]
        f_draw_layout_bbox = True
        f_draw_span_bbox = True
        parse_method = "vlm"
        pdf_bytes_list=[pdf_bytes]
        pdf_file_names=[input_file_name]
        for idx, pdf_bytes in enumerate(pdf_bytes_list):
            pdf_file_name = pdf_file_names[idx]
            pdf_bytes = convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
            local_image_dir, local_md_dir = prepare_env(output_dir, pdf_file_name, parse_method)
            image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)
            middle_json, infer_result = vlm_doc_analyze(pdf_bytes, image_writer=image_writer, backend=backend, server_url=server_url)

            pdf_info = middle_json["pdf_info"]

            _process_output(
                pdf_info, pdf_bytes, pdf_file_name, local_md_dir, local_image_dir,
                md_writer, f_draw_layout_bbox, f_draw_span_bbox, f_dump_orig_pdf,
                f_dump_md, f_dump_content_list, f_dump_middle_json, f_dump_model_output,
                f_make_md_mode, middle_json, infer_result, is_pipeline=False
            )


def _process_output(
        pdf_info,
        pdf_bytes,
        pdf_file_name,
        local_md_dir,
        local_image_dir,
        md_writer,
        f_draw_layout_bbox,
        f_draw_span_bbox,
        f_dump_orig_pdf,
        f_dump_md,
        f_dump_content_list,
        f_dump_middle_json,
        f_dump_model_output,
        f_make_md_mode,
        middle_json,
        model_output=None,
        is_pipeline=True
):
    if f_draw_layout_bbox:
        draw_layout_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_layout.pdf")

    if f_draw_span_bbox:
        draw_span_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_span.pdf")

    if f_dump_orig_pdf:
        md_writer.write(
            f"{pdf_file_name}_origin.pdf",
            pdf_bytes,
        )

    image_dir = str(os.path.basename(local_image_dir))#��ȡ·�������һ���ļ���Ŀ¼��

    if f_dump_md:
        make_func = pipeline_union_make if is_pipeline else vlm_union_make
        md_content_str = make_func(pdf_info, f_make_md_mode, image_dir)
        md_writer.write_string(
            f"{pdf_file_name}.md",
            md_content_str,
        )


    #local_image_dir:outpout_dir/filename/images
    if f_dump_content_list:
        make_func = pipeline_union_make if is_pipeline else vlm_union_make
        content_list = make_func(pdf_info, MakeMode.CONTENT_LIST, image_dir)#content_list中的image路径前缀
        md_writer.write_string(
            f"{pdf_file_name}_content_list.json",
            json.dumps(content_list, ensure_ascii=False, indent=4),
        )

    if f_dump_middle_json:
        md_writer.write_string(
            f"{pdf_file_name}_middle.json",
            json.dumps(middle_json, ensure_ascii=False, indent=4),
        )

    if f_dump_model_output:
        md_writer.write_string(
            f"{pdf_file_name}_model.json",
            json.dumps(model_output, ensure_ascii=False, indent=4),
        )

    logger.info(f"local output dir is {local_md_dir}")


def parse_doc( #供pipeline使用的函数接口
        input_path,#./test.py
        output_dir,
        lang="ch",
        backend="pipeline",
        method="auto",
        server_url=None,
        start_page_id=0,
        end_page_id=None
):
    try:
        """
        file_name_list = []
        pdf_bytes_list = []
        lang_list = []
        for path in path_list:
            file_name = str(Path(path).stem)#�ļ���
            pdf_bytes = read_fn(path)#�ֽ����ȡ��pdf�ļ�
            #�������ļ��б�
            file_name_list.append(file_name)
            pdf_bytes_list.append(pdf_bytes)
            lang_list.append(lang)
        """
        pdf_file_name=str(Path(input_path).stem)
        pdf_bytes=read_fn(input_path)
        do_parse(
            output_dir=output_dir,
            input_file_name=pdf_file_name,
            pdf_bytes=pdf_bytes,
            p_lang=lang,
            backend=backend,
            parse_method=method,
            server_url=server_url,
            start_page_id=start_page_id,
            end_page_id=end_page_id
        )
        #postProcessImages(output_dir,pdf_file_name)
        #insertDictInMD(output_dir,pdf_file_name)
        
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    # args
    '''
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    pdf_files_dir = os.path.join(__dir__, "pdfs")
    output_dir = os.path.join(__dir__, "output")
    pdf_suffixes = ["pdf"]
    image_suffixes = ["png", "jpeg", "jp2", "webp", "gif", "bmp", "jpg"]

    doc_path_list = []
    for doc_path in Path(pdf_files_dir).glob('*'):
        if guess_suffix_by_path(doc_path) in pdf_suffixes + image_suffixes:
            doc_path_list.append(doc_path)

    # os.environ['MINERU_MODEL_SOURCE'] = "modelscope"
    '''
    """Use pipeline mode if your environment does not support VLM"""

    poster_path="../posterData"
    output_dir="../posterDataOutput_vlm"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    for poster_file in Path(poster_path).iterdir():
        if poster_file.suffix.lower()==".pdf":
            pdf_path=poster_file.resolve()
            parse_doc(poster_file, output_dir, backend="pipeline",method="auto")
    
    #insertDictInMD(output_dir,"docsam")
    """To enable VLM mode, change the backend to 'vlm-xxx'"""
    # parse_doc(doc_path_list, output_dir, backend="vlm-transformers")  # more general.
    # parse_doc(doc_path_list, output_dir, backend="vlm-mlx-engine")  # faster than transformers in macOS 13.5+.
    # parse_doc(doc_path_list, output_dir, backend="vlm-vllm-engine")  # faster(engine).
    # parse_doc(doc_path_list, output_dir, backend="vlm-http-client", server_url="http://127.0.0.1:30000")  # faster(client).