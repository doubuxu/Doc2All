import pandas as pd
import random
from pathlib import Path
from pdf2image import convert_from_path

def generateIMG(pdf_path, output_path):
    """
    将单个 PDF 的第一页转换为 JPG 图片
    """
    pdf_path = Path(pdf_path)
    file_name = pdf_path.stem
    target_path = Path(output_path) / f"{file_name}.jpg"
    
    try:
        # 将 PDF 转换为图片列表（默认取第一页）
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            images[0].save(target_path, "JPEG")
            return True
    except Exception as e:
        print(f"转换文件 {file_name} 时出错: {e}")
        return False
    return False

def batchGenerateIMG(pdf_dir, output_path, number):
    pdf_dir = Path(pdf_dir)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    csv_path = pdf_dir / "conversion_status.csv"
    
    # 1. 获取目录下所有 PDF 文件
    all_pdfs = [f.name for f in pdf_dir.glob("*.pdf")]
    
    # 2. 初始化或读取 CSV 记录
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        # 检查是否有新加入目录的 PDF 文件
        existing_files = df['pdf_name'].tolist()
        new_files = [f for f in all_pdfs if f not in existing_files]
        if new_files:
            new_df = pd.DataFrame({'pdf_name': new_files, 'is_converted': False})
            df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = pd.DataFrame({'pdf_name': all_pdfs, 'is_converted': False})

    # 3. 筛选未转换的文件
    unconverted_df = df[df['is_converted'] == False]
    
    if unconverted_df.empty:
        print("所有 PDF 文件均已转换完成。")
        return

    # 4. 随机抽取指定数量的文件
    sample_size = min(len(unconverted_df), number)
    to_convert = unconverted_df.sample(n=sample_size)

    # 5. 循环转换并更新状态
    for idx, row in to_convert.iterrows():
        pdf_name = row['pdf_name']
        full_pdf_path = pdf_dir / pdf_name
        
        print(f"正在处理: {pdf_name}...")
        success = generateIMG(full_pdf_path, output_path)
        
        if success:
            df.at[idx, 'is_converted'] = True
            # 每成功转换一个就保存一次 CSV，防止程序意外中断导致进度丢失
            df.to_csv(csv_path, index=False)
            
    print(f"批处理完成，本次成功转换 {sample_size} 个文件。")

# 使用示例
# batchGenerateIMG("./data/pdfs", "./data/outputs", 5)

if __name__=="__main__":
    batchGenerateIMG("../f1000_posters/", "../posterData/batch3", 300)