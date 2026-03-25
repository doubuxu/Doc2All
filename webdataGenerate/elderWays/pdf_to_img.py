import fitz  # 对应 PyMuPDF
import os
from pathlib import Path

def batch_pdf_to_image(input_folder, output_folder, zoom_factor=2.0):
    """
    将文件夹下的单页 PDF 转换为同名图片
    :param input_folder: PDF 文件夹路径
    :param output_folder: 图片保存路径
    :param zoom_factor: 缩放倍数，2.0 对应 144 DPI (清晰度较高)
    """
    # 确保输出目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出目录: {output_folder}")

    # 获取所有 PDF 文件
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("未在文件夹中找到 PDF 文件。")
        return

    print(f"开始转换，共找到 {len(pdf_files)} 个文件...")

    # 设置缩放矩阵 (提高分辨率，否则默认 72 DPI 会很模糊)
    # zoom_x, zoom_y 分别为水平和垂直方向的缩放比例
    mat = fitz.Matrix(zoom_factor, zoom_factor)

    for pdf_name in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_name)
        
        try:
            # 打开 PDF
            doc = fitz.open(pdf_path)
            
            # 仅处理第一页 (针对单页 PDF)
            page = doc[0]
            
            # 获取页面的位图对象
            pix = page.get_pixmap(matrix=mat)
            
            # 生成输出文件名 (替换后缀为 .png)
            base_name = Path(pdf_name).stem
            output_path = os.path.join(output_folder, f"{base_name}.png")
            
            # 保存图片
            pix.save(output_path)
            print(f"成功: {pdf_name} -> {base_name}.png")
            
            doc.close()
        except Exception as e:
            print(f"错误: 处理 {pdf_name} 时发生异常: {e}")

# --- 配置参数 ---
input_dir = "../webData/web_pdf_2_final"  # 替换为你的 PDF 文件夹路径
output_dir = "../webData/imgs_2" # 替换为你想存放图片的路径

# 运行
if __name__ == "__main__":
    batch_pdf_to_image(input_dir, output_dir)