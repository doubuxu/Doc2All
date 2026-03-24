import os
from bs4 import BeautifulSoup

def calculate_image_path_ratio(html_path):
    """
    计算 HTML 中有效图片路径的比例。
    
    Args:
        html_path (str): 生成的 HTML 文件路径。
        
    Returns:
        float: 有效路径比例 (0.0 - 1.0)。如果没有图片标签，返回 1.0（表示无错误）。
    """
    # 获取 HTML 所在的基准目录
    base_dir = os.path.dirname(os.path.abspath(html_path))
    
    if not os.path.exists(html_path):
        return 0.0

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    img_tags = soup.find_all('img')
    total_imgs = len(img_tags)
    
    # 如果 HTML 里根本没用图片，视作路径逻辑满分
    if total_imgs == 0:
        return 1.0
    
    valid_count = 0
    
    for img in img_tags:
        src = img.get('src', '')
        
        # 1. 处理无需本地检查的情况（网络图或 Base64）
        if not src:
            continue
        if src.startswith(('http', 'https', 'data:')):
            valid_count += 1
            continue
            
        # 2. 拼接并检查本地路径
        full_path = os.path.normpath(os.path.join(base_dir, src))
        
        if os.path.exists(full_path):
            valid_count += 1
        # else:
        #    print(f"缺失文件: {full_path}") # 调试用

    # 计算比例
    return float(valid_count / total_imgs)

# 使用示例：
# score = calculate_image_path_ratio("output/poster_01.html")
# print(f"图片路径准确率: {score:.2%}")

if __name__=="__main__":
    html_path="../data/output/20260322_235110_sceneGraph_poster/sceneGraph.html"
    print(calculate_image_path_ratio(html_path))