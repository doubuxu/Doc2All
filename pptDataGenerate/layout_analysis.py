import os
import json
import subprocess
import shutil
from pptx import Presentation
from PIL import Image
from pdf2image import convert_from_path

def emu_to_px(emu):
    if emu is None: return 0
    return int(emu / 9144)

def ppt_to_pdf_libreoffice(ppt_path, output_dir):
    """单次调用 LibreOffice，将整个 PPT 转换为一个 PDF 文件"""
    print(f"  [Step 1] 正在通过 LibreOffice 转换 PDF...")
    abs_ppt_path = os.path.abspath(ppt_path)
    cmd = [
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, abs_ppt_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf_name = os.path.splitext(os.path.basename(ppt_path))[0] + ".pdf"
    return os.path.join(output_dir, pdf_name)

def crop_and_save(big_img, box, save_path):
    l, t, r, b = box
    l, t = max(0, l), max(0, t)
    r, b = min(big_img.width, r), min(big_img.height, b)
    if r > l and b > t:
        cropped = big_img.crop((l, t, r, b))
        cropped.save(save_path, "PNG")

def process_batch_ppts(input_folder, base_output_path):
    """
    批量处理文件夹下的所有 PPT/PPTX
    - 统一命名：非表格/非文本的视觉元素统一命名为 image_n.png
    - 兼容性：自动将旧版 .ppt 转换为 .pptx 进行解析
    """
    
    os.makedirs(base_output_path, exist_ok=True)
    ppt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.pptx', '.ppt'))]
    print(f"找到 {len(ppt_files)} 个待处理文件。")

    for ppt_file in ppt_files:
        ppt_path = os.path.join(input_folder, ppt_file)
        ppt_stem = os.path.splitext(ppt_file)[0]
        
        # 创建 PPT 同名根目录
        ppt_root_dir = os.path.join(base_output_path, ppt_stem)
        os.makedirs(ppt_root_dir, exist_ok=True)
        
        print(f"\n>>> 正在处理文件: {ppt_file}")

        # 临时工作目录，用于存放转换后的 PDF 和中间 PPTX
        temp_worker_dir = os.path.join(ppt_root_dir, "temp_worker")
        os.makedirs(temp_worker_dir, exist_ok=True)

        try:
            # --- 兼容性处理：如果是旧版 .ppt，先转为 .pptx ---
            if ppt_file.lower().endswith('.ppt'):
                print(f"  [Wait] 检测到旧版 PPT，正在预转换为 PPTX...")
                # 使用 LibreOffice 转换为 pptx
                convert_cmd = [
                    'libreoffice', '--headless', '--convert-to', 'pptx',
                    '--outdir', temp_worker_dir, os.path.abspath(ppt_path)
                ]
                subprocess.run(convert_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                working_ppt_path = os.path.join(temp_worker_dir, ppt_stem + ".pptx")
            else:
                working_ppt_path = ppt_path

            # 1. 生成 PDF 用于切图
            pdf_path = ppt_to_pdf_libreoffice(ppt_path, temp_worker_dir)
            
            # 2. 解析 PPT 结构
            prs = Presentation(working_ppt_path)
            total_slides = len(prs.slides)
            print(f"  [Step 2] 检测到 {total_slides} 页内容，开始逐页解析...")

            for page_index in range(total_slides):
                page_dir = os.path.join(ppt_root_dir, f"page_{page_index}")
                images_dir = os.path.join(page_dir, "images")
                tables_dir = os.path.join(page_dir, "tables")
                os.makedirs(images_dir, exist_ok=True)
                os.makedirs(tables_dir, exist_ok=True)

                # 提取 PDF 当前页高清图
                images = convert_from_path(
                    pdf_path, dpi=300, 
                    first_page=page_index + 1, 
                    last_page=page_index + 1
                )
                
                if not images: continue
                big_img = images[0]
                big_w, big_h = big_img.size
                big_img.save(os.path.join(page_dir, "full_slide.png"), "PNG")

                scale_x = big_w / emu_to_px(prs.slide_width)
                scale_y = big_h / emu_to_px(prs.slide_height)

                layout_data = {
                    "ppt_name": ppt_stem,
                    "page_index": page_index,
                    "full_image": "full_slide.png",
                    "canvas_size": {"width": big_w, "height": big_h},
                    "elements": []
                }

                # 统一计数器
                img_idx, table_idx = 1, 1
                slide = prs.slides[page_index]

                for shape in slide.shapes:
                    shape_type_code = int(shape.shape_type)
                    
                    # 过滤不需要的类型（如 Chart）
                    if shape_type_code == 3: continue
                    if shape_type_code == 14 and not shape.has_table: continue

                    l_px = int(emu_to_px(shape.left) * scale_x)
                    t_px = int(emu_to_px(shape.top) * scale_y)
                    w_px = int(emu_to_px(shape.width) * scale_x)
                    h_px = int(emu_to_px(shape.height) * scale_y)

                    element = {"bbox": {"left": l_px, "top": t_px, "width": w_px, "height": h_px}}

                    # --- 分类处理逻辑 ---
                    
                    # 1. 表格处理
                    if shape.has_table:
                        element["type"] = "table"
                        save_name = f"slide_{page_index}_table_{table_idx}.png"
                        crop_and_save(big_img, (l_px, t_px, l_px + w_px, t_px + h_px), os.path.join(tables_dir, save_name))
                        element["id"] = f"slide_{page_index}_table_{table_idx}"
                        element["path"] = f"tables/{save_name}"
                        table_idx += 1
                        layout_data["elements"].append(element)

                    # 2. 视觉元素处理 (图片 13, 组合 6, SmartArt 24, 形状等)
                    # 只要不是纯文本，且不是表格，都作为 image 导出
                    elif shape_type_code in [6, 13, 24] or (not shape.has_text_frame):
                        element["type"] = "image"
                        # 记录原始类型方便追溯
                        element["sub_type"] = "group" if shape_type_code == 6 else "picture"
                        
                        save_name = f"slide_{page_index}_image_{img_idx}.png"
                        crop_and_save(big_img, (l_px, t_px, l_px + w_px, t_px + h_px), os.path.join(images_dir, save_name))
                        element["id"] = f"slide_{page_index}_image_{img_idx}"
                        element["path"] = f"images/{save_name}"
                        img_idx += 1
                        layout_data["elements"].append(element)

                    # 3. 纯文本处理
                    elif shape.has_text_frame and shape.text.strip():
                        element["type"] = "text"
                        element["content"] = shape.text.strip()
                        layout_data["elements"].append(element)

                # 保存 JSON
                with open(os.path.join(page_dir, "layout.json"), "w", encoding="utf-8") as f:
                    json.dump(layout_data, f, indent=4, ensure_ascii=False)

            print(f"  [Done] 文件 {ppt_file} 处理完毕。")

        except Exception as e:
            print(f"  [Error] 处理文件 {ppt_file} 时出错: {e}")

        finally:
            # 清理临时转换文件
            if os.path.exists(temp_worker_dir):
                shutil.rmtree(temp_worker_dir)
            break
if __name__ == "__main__":
    # 配置你的路径
    INPUT_DIR = "../pptOriginalData"
    OUTPUT_DIR = "../pptDataOutput"
    
    process_batch_ppts(INPUT_DIR, OUTPUT_DIR)