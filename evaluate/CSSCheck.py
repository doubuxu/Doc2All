import cssutils
from bs4 import BeautifulSoup
import logging

# 屏蔽 cssutils 内部的解析警告，只获取结果
cssutils.log.setLevel(logging.CRITICAL)

def is_css_valid(html_path):
    """
    检查 HTML 中所有内联 CSS 样式是否合法
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    style_tags = soup.find_all(style=True)
    
    if not style_tags:
        return True # 如果没有样式，默认也是“合法”的
    
    for tag in style_tags:
        style_str = tag['style'].strip()
        if not style_str:
            continue
            
        # 解析 CSS 字符串
        sheet = cssutils.parseStyle(style_str)
        
        # 判定标准：
        # 1. 至少要能解析出属性 (Property)
        # 2. 如果原始字符串有内容但解析结果为空，说明全是乱码
        if len(sheet.keys()) == 0 and len(style_str) > 0:
            return False
            
        # 3. 检查是否有特定的解析错误（可选）
        # 如果模型输出了 invalid-color: 123; 这种完全错误的语法，sheet.valid 会为 False
        if not sheet.valid:
            return False
            
    return True

# 示例：
# html = '<div style="color: red; margin-top: 10px;">内容</div>' # True
# html_bad = '<div style="color: ;;; 123px">内容</div>' # False

if __name__=="__main__":
    html_path="../data/output/20260322_235110_sceneGraph_poster/sceneGraph.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(is_css_valid(content))
    
    