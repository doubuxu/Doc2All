import pandas as pd
from pathlib import Path

def changeCSV(csv_path, images_dir):
    """
    根据图片文件夹中的文件名更新 CSV 文件的 'used' 列
    """
    csv_path = Path(csv_path)
    images_dir = Path(images_dir)

    # 1. 读取原始 CSV 文件
    if not csv_path.exists():
        print(f"错误：找不到 CSV 文件 {csv_path}")
        return
    
    df = pd.read_csv(csv_path)

    # 2. 获取图片目录下所有 .png 文件的文件名（不带后缀）
    # 使用 set 可以显著提高后续查找速度
    image_filenames = {f.stem for f in images_dir.glob("*.png")}

    # 3. 增加或更新 'used' 列
    # 首先默认全部设为 False
    df['used'] = False
    
    # 4. 如果 CSV 中的 title 在图片文件名集合中，则设为 True
    # 使用 .isin() 是一种高效的批量处理方式
    df.loc[df['title'].astype(str).isin(image_filenames), 'used'] = True

    # 5. 写回 CSV 文件
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"CSV 更新完成。共标记 {df['used'].sum()} 个文件为 True。")
    except Exception as e:
        print(f"保存 CSV 时出错: {e}")

# 使用示例
if __name__=="__main__":
    changeCSV("url.csv", "../webData/imgs_2")
