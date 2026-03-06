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
    """批量处理文件夹下的所有 PPT/PPTX"""
    
    # 确保输出总目录存在
    os.makedirs(base_output_path, exist_ok=True)
    
    # 获取所有 PPT 文件
    ppt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.pptx', '.ppt'))]
    print(f"找到 {len(ppt_files)} 个待处理文件。")

    for ppt_file in ppt_files:
        ppt_path = os.path.join(input_folder, ppt_file)
        ppt_stem = os.path.splitext(ppt_file)[0]
        print(f"\n>>> 正在处理文件: {ppt_file}")

        # 1. 为当前 PPT 创建临时 PDF 目录
        temp_pdf_dir = os.path.join(base_output_path, f"temp_pdf_{ppt_stem}")
        os.makedirs(temp_pdf_dir, exist_ok=True)

        try:
            # 2. 一次性生成整份 PDF
            pdf_path = ppt_to_pdf_libreoffice(ppt_path, temp_pdf_dir)
            
            # 3. 使用 python-pptx 获取总页数
            prs = Presentation(ppt_path)
            total_slides = len(prs.slides)
            print(f"  [Step 2] 检测到 {total_slides} 页内容，开始逐页解析...")

            # 4. 逐页处理
            for page_index in range(total_slides):
                page_folder_name = f"{ppt_stem}_{page_index}"
                page_dir = os.path.join(base_output_path, page_folder_name)
                
                # 准备子目录
                images_dir = os.path.join(page_dir, "images")
                tables_dir = os.path.join(page_dir, "tables")
                os.makedirs(images_dir, exist_ok=True)
                os.makedirs(tables_dir, exist_ok=True)

                # 5. 从 PDF 提取当前页的高清大图 (DPI=300)
                # pdf2image 的 first_page 和 last_page 都是 1-indexed
                images = convert_from_path(
                    pdf_path, dpi=300, 
                    first_page=page_index + 1, 
                    last_page=page_index + 1
                )
                
                if not images:
                    print(f"    [!] 第 {page_index} 页转换大图失败，跳过。")
                    continue

                big_img = images[0]
                big_w, big_h = big_img.size
                big_image_path = os.path.join(page_dir, f"{page_folder_name}_full.png")
                big_img.save(big_image_path, "PNG")

                # 6. 解析 PPT 布局
                slide = prs.slides[page_index]
                scale_x = big_w / emu_to_px(prs.slide_width)
                scale_y = big_h / emu_to_px(prs.slide_height)

                layout_data = {
                    "ppt_name": ppt_stem,
                    "page_index": page_index,
                    "full_image": f"{page_folder_name}_full.png",
                    "canvas_size": {"width": big_w, "height": big_h},
                    "elements": []
                }

                img_idx, table_idx = 1, 1

                for shape in slide.shapes:
                    shape_type_code = int(shape.shape_type)
                    
                    # 过滤逻辑：只跳过图表(3)，不再跳过组合(6)
                    if shape_type_code in [3]: continue
                    # 过滤非表格的 Graphic Frame (14)
                    if shape_type_code == 14 and not shape.has_table: continue

                    l_px = int(emu_to_px(shape.left) * scale_x)
                    t_px = int(emu_to_px(shape.top) * scale_y)
                    w_px = int(emu_to_px(shape.width) * scale_x)
                    h_px = int(emu_to_px(shape.height) * scale_y)

                    element = {"bbox": {"left": l_px, "top": t_px, "width": w_px, "height": h_px}}

                    # --- 新增：处理 SmartArt (24) 和 组合形状 (6) ---
                    if shape_type_code == 24 or shape_type_code == 6:
                        tag = "smartart" if shape_type_code == 24 else "group"
                        element["type"] = tag
                        save_name = f"{tag}_{img_idx}.png"
                        # 从大图中根据组合/SmartArt的总边界进行裁剪
                        crop_and_save(big_img, (l_px, t_px, l_px + w_px, t_px + h_px), os.path.join(images_dir, save_name))
                        element["id"] = f"{tag}_{img_idx}"
                        element["path"] = f"images/{save_name}"
                        img_idx += 1
                        layout_data["elements"].append(element)

                    # 表格
                    elif shape.has_table:
                        element["type"] = "table"
                        save_name = f"table_{table_idx}.png"
                        crop_and_save(big_img, (l_px, t_px, l_px + w_px, t_px + h_px), os.path.join(tables_dir, save_name))
                        element["id"] = f"table_{table_idx}"
                        element["path"] = f"tables/{save_name}"
                        table_idx += 1
                        layout_data["elements"].append(element)

                    # 图片 (13=Picture)
                    elif shape_type_code == 13:
                        element["type"] = "image"
                        save_name = f"image_{img_idx}.png"
                        crop_and_save(big_img, (l_px, t_px, l_px + w_px, t_px + h_px), os.path.join(images_dir, save_name))
                        element["id"] = f"image_{img_idx}"
                        element["path"] = f"images/{save_name}"
                        img_idx += 1
                        layout_data["elements"].append(element)

                    # 文本
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
            # 清理当前 PPT 的临时 PDF
            if os.path.exists(temp_pdf_dir):
                shutil.rmtree(temp_pdf_dir)

if __name__ == "__main__":
    # 配置你的路径
    INPUT_DIR = "../pptOriginalData"
    OUTPUT_DIR = "../pptDataOutput"
    
    process_batch_ppts(INPUT_DIR, OUTPUT_DIR)