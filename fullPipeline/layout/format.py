import os
from pathlib import Path
from PIL import Image
import argparse


def convert_jpg_to_pdf(input_folder, output_folder):
    """
    将指定文件夹中的所有 JPG 文件转换为同名的 PDF 文件
    
    参数:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径
    """
    # 确保输入文件夹存在
    if not os.path.exists(input_folder):
        print(f"错误: 输入文件夹 '{input_folder}' 不存在")
        return
    
    # 创建输出文件夹(如果不存在)
    os.makedirs(output_folder, exist_ok=True)
    
    # 支持的 JPG 扩展名(不区分大小写)
    jpg_extensions = {'.jpg', '.jpeg'}
    
    # 统计转换数量
    converted_count = 0
    error_count = 0
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # 跳过非文件项
        if not os.path.isfile(file_path):
            continue
        
        # 获取文件扩展名(转换为小写)
        file_ext = Path(filename).suffix.lower()
        
        # 检查是否为 JPG 文件
        if file_ext in jpg_extensions:
            try:
                # 获取不带扩展名的文件名
                file_stem = Path(filename).stem
                
                # 构建输出 PDF 文件路径
                output_pdf_path = os.path.join(output_folder, f"{file_stem}.pdf")
                
                # 打开 JPG 图片
                image = Image.open(file_path)
                
                # 如果图片是 RGBA 模式,转换为 RGB
                if image.mode == 'RGBA':
                    # 创建白色背景
                    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])  # 使用 alpha 通道作为遮罩
                    image = rgb_image
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # 保存为 PDF
                image.save(output_pdf_path, 'PDF', resolution=100.0)
                
                print(f"✓ 已转换: {filename} -> {file_stem}.pdf")
                converted_count += 1
                
            except Exception as e:
                print(f"✗ 转换失败 {filename}: {str(e)}")
                error_count += 1
    
    # 输出统计信息
    print(f"\n转换完成!")
    print(f"成功: {converted_count} 个文件")
    if error_count > 0:
        print(f"失败: {error_count} 个文件")


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='将文件夹中的所有 JPG 文件转换为 PDF 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python script.py -i ./images -o ./pdfs
  python script.py --input /path/to/images --output /path/to/pdfs
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入文件夹路径(包含 JPG 文件)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='输出文件夹路径(保存 PDF 文件)'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行转换
    convert_jpg_to_pdf(args.input, args.output)


if __name__ == '__main__':
    main()