# Copyright (c) Opendatalab. All rights reserved.
import copy
import json
import os
# 将显存占用率从 0.5 降低到 0.2 或 0.3
os.environ['MINERU_VLLM_GPU_MEM'] = "0.1"
from pathlib import Path
import shutil

from loguru import logger

from mineru.cli.common import convert_pdf_bytes_to_bytes_by_pypdfium2, prepare_env, read_fn
from mineru.data.data_reader_writer import FileBasedDataWriter 
from mineru.utils.draw_bbox import draw_layout_bbox, draw_span_bbox
from mineru.utils.engine_utils import get_vlm_engine
from mineru.utils.enum_class import MakeMode
from mineru.backend.vlm.vlm_analyze import doc_analyze as vlm_doc_analyze
from mineru.backend.pipeline.pipeline_analyze import doc_analyze as pipeline_doc_analyze
from mineru.backend.pipeline.pipeline_middle_json_mkcontent import union_make as pipeline_union_make
from mineru.backend.pipeline.model_json_to_middle_json import result_to_middle_json as pipeline_result_to_middle_json
from mineru.backend.vlm.vlm_middle_json_mkcontent import union_make as vlm_union_make
from mineru.backend.hybrid.hybrid_analyze import doc_analyze as hybrid_doc_analyze
from mineru.utils.guess_suffix_or_lang import guess_suffix_by_path


def do_parse(
    output_dir,  # Output directory for storing parsing results
    pdf_file_names: list[str],  # List of PDF file names to be parsed
    pdf_bytes_list: list[bytes],  # List of PDF bytes to be parsed
    p_lang_list: list[str],  # List of languages for each PDF, default is 'ch' (Chinese)
    backend="hybrid-auto-engine",  # The backend for parsing PDF, default is 'hybrid-auto-engine'
    parse_method="auto",  # The method for parsing PDF, default is 'auto'
    formula_enable=True,  # Enable formula parsing
    table_enable=True,  # Enable table parsing
    server_url=None,  # Server URL for vlm-http-client backend
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
        for idx, pdf_bytes in enumerate(pdf_bytes_list):
            new_pdf_bytes = convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
            pdf_bytes_list[idx] = new_pdf_bytes

        infer_results, all_image_lists, all_pdf_docs, lang_list, ocr_enabled_list = pipeline_doc_analyze(pdf_bytes_list, p_lang_list, parse_method=parse_method, formula_enable=formula_enable,table_enable=table_enable)

        for idx, model_list in enumerate(infer_results):
            model_json = copy.deepcopy(model_list)
            pdf_file_name = pdf_file_names[idx]
            local_image_dir, local_md_dir = prepare_env(output_dir, pdf_file_name, parse_method)
            image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)

            images_list = all_image_lists[idx]
            pdf_doc = all_pdf_docs[idx]
            _lang = lang_list[idx]
            _ocr_enable = ocr_enabled_list[idx]
            middle_json = pipeline_result_to_middle_json(model_list, images_list, pdf_doc, image_writer, _lang, _ocr_enable, formula_enable)

            pdf_info = middle_json["pdf_info"]

            pdf_bytes = pdf_bytes_list[idx]
            _process_output(
                pdf_info, pdf_bytes, pdf_file_name, local_md_dir, local_image_dir,
                md_writer, f_draw_layout_bbox, f_draw_span_bbox, f_dump_orig_pdf,
                f_dump_md, f_dump_content_list, f_dump_middle_json, f_dump_model_output,
                f_make_md_mode, middle_json, model_json, is_pipeline=True
            )
    else:
        f_draw_span_bbox = False

        if backend.startswith("vlm-"):
            backend = backend[4:]

            if backend == "auto-engine":
                backend = get_vlm_engine(inference_engine='auto', is_async=False)

            parse_method = "vlm"
            for idx, pdf_bytes in enumerate(pdf_bytes_list):
                pdf_file_name = pdf_file_names[idx]
                pdf_bytes = convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
                local_image_dir, local_md_dir = prepare_env(output_dir, pdf_file_name, parse_method)
                print(f"local_image_dir:{local_image_dir}")
                print(f"local_md_dir:{local_md_dir}")
                image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)
                middle_json, infer_result = vlm_doc_analyze(pdf_bytes, image_writer=image_writer, backend=backend, server_url=server_url)

                pdf_info = middle_json["pdf_info"]

                _process_output(
                    pdf_info, pdf_bytes, pdf_file_name, local_md_dir, local_image_dir,
                    md_writer, f_draw_layout_bbox, f_draw_span_bbox, f_dump_orig_pdf,
                    f_dump_md, f_dump_content_list, f_dump_middle_json, f_dump_model_output,
                    f_make_md_mode, middle_json, infer_result, is_pipeline=False
                )
        elif backend.startswith("hybrid-"):
            backend = backend[7:]

            if backend == "auto-engine":
                backend = get_vlm_engine(inference_engine='auto', is_async=False)

            parse_method = f"hybrid_{parse_method}"
            for idx, pdf_bytes in enumerate(pdf_bytes_list):
                pdf_file_name = pdf_file_names[idx]
                pdf_bytes = convert_pdf_bytes_to_bytes_by_pypdfium2(pdf_bytes, start_page_id, end_page_id)
                local_image_dir, local_md_dir = prepare_env(output_dir, pdf_file_name, parse_method)
                image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)
                middle_json, infer_result, _vlm_ocr_enable = hybrid_doc_analyze(
                    pdf_bytes,
                    image_writer=image_writer,
                    backend=backend,
                    parse_method=parse_method,
                    language=p_lang_list[idx],
                    inline_formula_enable=formula_enable,
                    server_url=server_url,
                )

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
    """处理输出文件"""
    if f_draw_layout_bbox:
        draw_layout_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_layout.pdf")

    if f_draw_span_bbox:
        draw_span_bbox(pdf_info, pdf_bytes, local_md_dir, f"{pdf_file_name}_span.pdf")

    if f_dump_orig_pdf:
        md_writer.write(
            f"{pdf_file_name}_origin.pdf",
            pdf_bytes,
        )

    image_dir = str(os.path.basename(local_image_dir))
    #image_dir =Path(image_dir).resolve()
    if f_dump_md:
        make_func = pipeline_union_make if is_pipeline else vlm_union_make
        md_content_str = make_func(pdf_info, f_make_md_mode, image_dir)
        md_writer.write_string(
            f"{pdf_file_name}.md",
            md_content_str,
        )

    if f_dump_content_list:
        make_func = pipeline_union_make if is_pipeline else vlm_union_make
        content_list = make_func(pdf_info, MakeMode.CONTENT_LIST, image_dir)
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


def parse_doc(
        path_list: list[Path],
        output_dir,
        lang="ch",
        backend="hybrid-auto-engine",
        method="auto",
        server_url=None,
        start_page_id=0,
        end_page_id=None
):
    """
        Parameter description:
        path_list: List of document paths to be parsed, can be PDF or image files.
        output_dir: Output directory for storing parsing results.
        lang: Language option, default is 'ch', optional values include['ch', 'ch_server', 'ch_lite', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'th', 'el',
                       'latin', 'arabic', 'east_slavic', 'cyrillic', 'devanagari']。
            Input the languages in the pdf (if known) to improve OCR accuracy.  Optional.
            Adapted only for the case where the backend is set to 'pipeline' and 'hybrid-*'
        backend: the backend for parsing pdf:
            pipeline: More general.
            vlm-auto-engine: High accuracy via local computing power.
            vlm-http-client: High accuracy via remote computing power(client suitable for openai-compatible servers).
            hybrid-auto-engine: Next-generation high accuracy solution via local computing power.
            hybrid-http-client: High accuracy but requires a little local computing power(client suitable for openai-compatible servers).
            Without method specified, hybrid-auto-engine will be used by default.
        method: the method for parsing pdf:
            auto: Automatically determine the method based on the file type.
            txt: Use text extraction method.
            ocr: Use OCR method for image-based PDFs.
            Without method specified, 'auto' will be used by default.
            Adapted only for the case where the backend is set to 'pipeline' and 'hybrid-*'.
        server_url: When the backend is `http-client`, you need to specify the server_url, for example:`http://127.0.0.1:30000`
        start_page_id: Start page ID for parsing, default is 0
        end_page_id: End page ID for parsing, default is None (parse all pages until the end of the document)
    """
    try:
        file_name_list = []
        pdf_bytes_list = []
        lang_list = []
        for path in path_list:
            file_name = str(Path(path).stem)
            pdf_bytes = read_fn(path)
            file_name_list.append(file_name)
            pdf_bytes_list.append(pdf_bytes)
            lang_list.append(lang)
        do_parse(
            output_dir=output_dir,
            pdf_file_names=file_name_list,
            pdf_bytes_list=pdf_bytes_list,
            p_lang_list=lang_list,
            backend=backend,
            parse_method=method,
            server_url=server_url,
            start_page_id=start_page_id,
            end_page_id=end_page_id
        )
    except Exception as e:
        logger.exception(e)


def flatten_run_mode_dir(output_path, pdf_file_name, run_mode="hybrid_auto"):
    doc_dir = Path(output_path) / pdf_file_name
    mode_dir = doc_dir / run_mode

    if not mode_dir.exists():
        raise FileNotFoundError(f"{mode_dir} does not exist")

    for item in mode_dir.iterdir():
        target = doc_dir / item.name
        if target.exists():
            raise RuntimeError(f"Target already exists: {target}")
        shutil.move(str(item), str(target))

    mode_dir.rmdir()

import json
from pathlib import Path

def patch_equation_paths_from_middle(content_json_path: str, middle_json_path: str):
    """
    专门针对公式（equation）进行路径补全。
    匹配逻辑：从 middle.json 的 pdf_info[0]['para_blocks'] 中寻找 type='interline_equation' 的 span
    """
    import json
    from pathlib import Path

    content_json_path = Path(content_json_path)
    middle_json_path = Path(middle_json_path)

    # ===== 读取文件 =====
    with open(content_json_path, "r", encoding="utf-8") as f:
        content_list = json.load(f)

    with open(middle_json_path, "r", encoding="utf-8") as f:
        middle_data = json.load(f)

    # ===== 提取 middle.json 中的公式图片路径 =====
    # 根据你提供的结构：middle_data['pdf_info'] 是一个列表
    equation_image_paths = []
    
    pdf_info = middle_data.get("pdf_info", [])
    for page in pdf_info:
        blocks = page.get("para_blocks", [])
        for block in blocks:
            # 仅处理行间公式类型
            if block.get("type") == "interline_equation":
                lines = block.get("lines", [])
                for line in lines:
                    spans = line.get("spans", [])
                    for span in spans:
                        # 提取 span 里的 image_path
                        img_p = span.get("image_path")
                        if img_p:
                            equation_image_paths.append(img_p)

    # ===== 将路径回填至 content_list.json =====
    eq_index = 0
    total_middle_eq = len(equation_image_paths)

    for item in content_list:
        # 只处理 content_list 中类型为 equation 的条目
        if item.get("type") == "equation":
            if eq_index < total_middle_eq:
                # 保持与你后续 reorganize_path 逻辑一致的前缀
                item["img_path"] = f"images/{equation_image_paths[eq_index]}"
                eq_index += 1
            else:
                # 如果 middle 里的公式用完了，设为空防止指向错误
                item["img_path"] = ""

    # ===== 写回文件 =====
    with open(content_json_path, "w", encoding="utf-8") as f:
        json.dump(content_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 公式路径补全完成: 已匹配 {eq_index} 个，Middle中共找到 {total_middle_eq} 个。")
    return content_list

def fix_paths_in_content_list(json_path: str):
    json_path = Path(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        # 图片
        if "img_path" in item and item["img_path"]:
            item["img_path"] = item["img_path"].replace("hybrid_auto/", "")

        # 表格
        if "table_path" in item and item["table_path"]:
            item["table_path"] = item["table_path"].replace("hybrid_auto/", "")

        # 公式
        if "equation_path" in item and item["equation_path"]:
            item["equation_path"] = item["equation_path"].replace("hybrid_auto/", "")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fix_visual_index_paths(json_path: str):
    json_path = Path(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        if "path" in item and item["path"]:
            item["path"] = item["path"].replace("hybrid_auto/", "")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reorganize_path(doc_path_list,output_path):
    pdf_files_path=doc_path_list[0]
    pdf_file_name=Path(pdf_files_path).name
    pdf_file_name = pdf_file_name[:-4]
    content_list_path = Path(output_path) / pdf_file_name / "hybrid_auto" / f"{pdf_file_name}_content_list.json"
    middle_json_path = Path(output_path) / pdf_file_name / "hybrid_auto" / f"{pdf_file_name}_middle.json"
    content_list = patch_equation_paths_from_middle(content_list_path, middle_json_path)
    #with open(content_list_path,'r',encoding='utf-8') as f:
    #    content_list = json.load(f)
    images_list=[]
    tables_list=[]
    equations_list=[]
    images_name=[]
    tables_name=[]
    equations_name=[]
    fig_index=1
    table_index=1
    eq_index=1
    for index,entity in enumerate(content_list):
        if entity["type"] == "image" :
           image_info={
                        "fig_id":f"fig_{fig_index}",
                        "path": entity["img_path"],
                        "caption":entity["image_caption"],
                        "content_list_index":index
                }
           images_name.append(Path(entity["img_path"]).name)
           images_list.append(image_info)
           fig_index+=1
        elif entity["type"] == "table" :
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
        elif entity["type"] == "equation" :
            equations_info={
                        "equations_id":f"equations_{eq_index}",
                        "path":entity["img_path"],
                        "content_list_index":index
                }
            equations_name.append(Path(entity["img_path"]).name)
            equations_list.append(equations_info)
            eq_index+=1
    
    
    images_dir = Path(output_path) / pdf_file_name / "hybrid_auto"/"visuals" / "images"
    tables_dir = Path(output_path) / pdf_file_name / "hybrid_auto"/"visuals" / "tables"
    eq_dirs = Path(output_path) / pdf_file_name / "hybrid_auto"/"visuals" / "equations"
    os.makedirs(images_dir,exist_ok=True)
    os.makedirs(tables_dir,exist_ok=True)
    os.makedirs(eq_dirs,exist_ok=True)
    visuals_path=Path(output_path) / pdf_file_name / "hybrid_auto" / "images"
    md_path=Path(output_path) / pdf_file_name / "hybrid_auto" / f"{pdf_file_name}.md"
    md_dir=md_path.parent
    md_content_str = md_path.read_text(encoding='utf-8')
    for file in visuals_path.iterdir():
        file=file.resolve()
        print(file)
        name=Path(file).name
        if name in images_name:
            index=images_name.index(name)
            new_name=images_list[index]["fig_id"]+".jpg"
                    
            dst=images_dir/new_name
            #print(f"new_path:{dst}")
            shutil.move(str(file),str(dst))
            old_rel = os.path.relpath(file, md_dir)
            new_rel = Path(str(dst).replace("/hybrid_auto/", "/")).as_posix()
            images_list[index]["path"]=str(dst)
            content_list_index=images_list[index]["content_list_index"]
            content_list[content_list_index]["img_path"]=str(dst)#替换content_list中的图片路径
            md_content_str=md_content_str.replace(old_rel.replace("\\", "/"),new_rel.replace("\\", "/"))
        elif name in tables_name:
            index=tables_name.index(name)
            new_name=tables_list[index]["table_id"]+".jpg"
                    
            dst=tables_dir/new_name
                    #print(f"new_path:{dst}")
            shutil.move(str(file),str(dst))
            old_rel = os.path.relpath(file, md_dir)
            new_rel = Path(str(dst).replace("/hybrid_auto/", "/")).as_posix()
            tables_list[index]["path"]=str(dst)
            content_list_index=tables_list[index]["content_list_index"]
            content_list[content_list_index]["img_path"]=str(dst)
            md_content_str=md_content_str.replace(old_rel.replace("\\", "/"),new_rel.replace("\\", "/"))
        elif name in equations_name:
            index=equations_name.index(name)
            new_name=equations_list[index]["equations_id"]+".jpg"
                    
            dst = eq_dirs / new_name
            #print(f"new_path:{dst}")
            shutil.move(str(file),str(dst))
            old_rel = os.path.relpath(file, md_dir)
            new_rel = Path(str(dst).replace("/hybrid_auto/", "/")).as_posix()
            equations_list[index]["path"]=str(dst)
            content_list_index=equations_list[index]["content_list_index"]
            content_list[content_list_index]["img_path"]=str(dst)
            md_content_str=md_content_str.replace(old_rel.replace("\\", "/"),new_rel.replace("\\", "/"))
    print(images_list)
    dict_path=Path(output_path)/ pdf_file_name / "hybrid_auto"/"dict"
    os.makedirs(dict_path, exist_ok=True)
    with open(dict_path/"images.json",'w',encoding='utf-8') as f:
        json.dump(images_list,f,ensure_ascii=False, indent=2)
            
    with open(dict_path/"tables.json",'w',encoding='utf-8') as f:
        json.dump(tables_list,f,ensure_ascii=False, indent=2)

    with open(dict_path/"equations.json",'w',encoding='utf-8') as f:
        json.dump(equations_list,f,ensure_ascii=False, indent=2)
    with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content_str)
    with open(content_list_path,'w',encoding='utf-8') as f:
        json.dump(content_list,f,ensure_ascii=False,indent=2)
    original_images_path=Path(output_path) / pdf_file_name / "hybrid_auto" / "images"
    shutil.rmtree(original_images_path)
    flatten_run_mode_dir(output_path,pdf_file_name)
    content_list_path = Path(output_path) / pdf_file_name / f"{pdf_file_name}_content_list.json"
    fix_paths_in_content_list(content_list_path)
    images_dict_path=Path(output_path)/ pdf_file_name / "dict" / "images.json"
    tables_dict_path=Path(output_path)/ pdf_file_name / "dict" / "tables.json"
    eq_dict_path=Path(output_path)/ pdf_file_name / "dict" / "equations.json"
    fix_visual_index_paths(images_dict_path)
    fix_visual_index_paths(tables_dict_path)
    fix_visual_index_paths(eq_dict_path)

def mineru_process(pdf_files_path,output_dir):
    doc_path_list=[pdf_files_path]
    parse_doc(doc_path_list, output_dir, backend="hybrid-auto-engine")
    reorganize_path(doc_path_list,output_dir)

if __name__ == '__main__':
    # args
    #__dir__ = os.path.dirname(os.path.abspath(__file__))
    pdf_files_path = '../posterData/batch6/'
    output_dir = '../posterData/batch6/mineru_output_with_eq'
    pdf_suffixes = ["pdf"]
    image_suffixes = ["png", "jpeg", "jp2", "webp", "gif", "bmp", "jpg"]

    #doc_path_list = []
    #for doc_path in Path(pdf_files_dir).glob('*'):
    #    if guess_suffix_by_path(doc_path) in pdf_suffixes + image_suffixes:
    #        doc_path_list.append(doc_path)

    """如果您由于网络问题无法下载模型，可以设置环境变量MINERU_MODEL_SOURCE为modelscope使用免代理仓库下载模型"""
    # os.environ['MINERU_MODEL_SOURCE'] = "modelscope"

    """Use hybrid mode and local computing power to parse documents"""
    for item in os.listdir(Path(pdf_files_path)):
        if item.lower().endswith(('.jpg', '.jpeg','.png')):
            file_path = os.path.join(pdf_files_path, item)

            doc_path_list=[file_path]
            parse_doc(doc_path_list, output_dir, backend="hybrid-auto-engine")
            reorganize_path(doc_path_list,output_dir)
    """Other backends for parsing documents, you can uncomment and try"""
    # parse_doc(doc_path_list, output_dir, backend="pipeline")  # more general.
    # parse_doc(doc_path_list, output_dir, backend="vlm-auto-engine")  # high accuracy via local computing power.
    # parse_doc(doc_path_list, output_dir, backend="vlm-http-client", server_url="http://127.0.0.1:30000")  # high accuracy via remote computing power(client suitable for openai-compatible servers).
    # parse_doc(doc_path_list, output_dir, backend="hybrid-http-client", server_url="http://127.0.0.1:30000")  # high accuracy but requires a little local computing power(client suitable for openai-compatible servers).