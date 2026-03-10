import os
import re
from bs4 import BeautifulSoup

def process_css_scoped(css_text, slide_id):
    """
    优化后的CSS隔离函数。
    将 .ppt-slide 替换为 #slide-n.ppt-slide (无空格)
    将其他选择器替换为 #slide-n.ppt-slide 选择器
    """
    # 移除注释
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    
    # 核心修复：处理 .ppt-slide 自身的样式定义
    css_text = css_text.replace('.ppt-slide', f'#{slide_id}.ppt-slide')
    
    # 处理其他内部选择器 (例如 .sidebar -> #slide-n.ppt-slide .sidebar)
    # 匹配非大括号内的字符作为选择器
    def add_scope(match):
        selector = match.group(1).strip()
        if selector.startswith(f'#{slide_id}') or selector.startswith('@'):
            return f"{selector} "
        return f"#{slide_id}.ppt-slide {selector} "

    scoped_css = re.sub(r'([^{}]+)(?=\{)', add_scope, css_text)
    return scoped_css

def merge_html_files(input_folder, output_file):
    # 1. 获取并按序号排序文件
    html_files = [f for f in os.listdir(input_folder) if f.endswith('.html')]
    html_files.sort(key=lambda x: int(re.search(r'_(\d+)\.html$', x).group(1)))

    all_slides_content = []
    all_css_content = []

    for i, filename in enumerate(html_files):
        slide_id = f"slide-{i+1}"
        file_path = os.path.join(input_folder, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
            # 提取并处理 CSS
            style_tag = soup.find('style')
            if style_tag:
                scoped_css = process_css_scoped(style_tag.string, slide_id)
                all_css_content.append(scoped_css)
            
            # 提取内容
            slide_div = soup.find('div', class_='ppt-slide')
            if slide_div:
                # 移除原始 ID 避免冲突，设置新的隔离 ID
                slide_div['id'] = slide_id
                # 基础类名用于控制显示/隐藏
                slide_div['class'] = "ppt-slide merged-slide"
                if i == 0:
                    slide_div['class'] += " active"
                
                # 注入一个 transform 容器，解决不同分辨率(1200px vs 1280px)的适配问题
                # 让内容自动在 16:9 的框架内居中缩小
                inner_content = slide_div.decode_contents()
                wrapped_content = f"""
                <div class="slide-scaler-wrapper">
                    {inner_content}
                </div>
                """
                slide_div.clear()
                slide_div.append(BeautifulSoup(wrapped_content, 'html.parser'))
                
                all_slides_content.append(str(slide_div))

    # 2. 最终模板
    final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PPT 合并演示文稿</title>
    <style>
        body, html {{ margin: 0; padding: 0; background: #1a1a1a; width: 100%; height: 100%; overflow: hidden; }}
        
        /* 16:9 主容器 */
        .presentation-root {{
            width: 100vw; height: 56.25vw; 
            max-width: 177.78vh; max-height: 100vh;
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background: #000; overflow: hidden;
            container-type: size;
        }}

        .merged-slide {{
            display: none !important; width: 100%; height: 100%;
            position: absolute; top: 0; left: 0;
        }}
        
        .merged-slide.active {{
            display: flex !important;
        }}

        /* 缩放适配层：确保不同px定义的画布能自适应 */
        .slide-scaler-wrapper {{
            width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center;
            transform-origin: center;
        }}

        /* 注入各页隔离样式 */
        {" ".join(all_css_content)}
    </style>
</head>
<body>
    <div class="presentation-root" id="presentation">
        {" ".join(all_slides_content)}
    </div>

    <script>
        const slides = document.querySelectorAll('.merged-slide');
        let current = 0;

        function show(index) {{
            slides[current].classList.remove('active');
            current = (index + slides.length) % slides.length;
            slides[current].classList.add('active');
        }}

        document.getElementById('presentation').onclick = () => show(current + 1);
        
        document.onkeydown = (e) => {{
            if(e.key === "ArrowRight" || e.key === " ") show(current + 1);
            if(e.key === "ArrowLeft") show(current - 1);
        }};
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Successfully merged {len(html_files)} slides into {output_file}")

# 执行合并
# merge_html_files('./your_input_folder', './final_ppt.html')
# 使用示例
# merge_ppt_html('./input_slides', './output/my_presentation.html')

if __name__=="__main__":
    input_html_path="./html_test"
    output_path='./merge.html'
    merge_html_files(input_html_path,output_path)