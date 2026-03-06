import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from bs4 import BeautifulSoup
import json
import re
from utils.JsonTools import save_json,load_json


def html_to_content_plan(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. 初始化 content_plan 结构，确保 metadata 符合你的新设计
    content_plan = {
        "metadata": {
            "title": "",
            "authors": [],
            "organizations": [],
            "github": "",
            "figures": []
        },
        "sections": []
    }

    # 2. 提取细化后的 Metadata
    header = soup.find('header')
    if header:
        # 标题
        title_el = header.find(class_='poster-title')
        if title_el:
            content_plan["metadata"]["title"] = title_el.get_text(strip=True)
        
        # 作者 (处理可能存在的逗号或分号分隔)
        authors_el = header.find(class_='poster-authors')
        if authors_el:
            authors_raw = authors_el.get_text(strip=True)
            # 尝试分割作者，如 "A, B, C" -> ["A", "B", "C"]
            authors_list = [a.strip() for a in re.split(r'[,;，；]', authors_raw) if a.strip()]
            content_plan["metadata"]["authors"] = authors_list
        
        # 机构与 GitHub (通常在 header-logos 或其他 div 中)
        logos_area = header.find(class_='header-logos')
        if logos_area:
            # 查找所有文本节点作为机构信息
            for div in logos_area.find_all('div', recursive=False):
                text = div.get_text(strip=True)
                if text:
                    # 简单逻辑：如果包含 github.com 则放入 github 字段，否则放入 organizations
                    if "github.com" in text.lower() or "git.io" in text.lower():
                        # 尝试提取 URL
                        github_match = re.search(r'(https?://github\.com/[^\s]+)', text)
                        content_plan["metadata"]["github"] = github_match.group(1) if github_match else text
                    else:
                        content_plan["metadata"]["organizations"].append(text)
            
            # 查找 header 区域内的图片 (如 Logo)
            header_imgs = logos_area.find_all('img')
            for img in header_imgs:
                img_src = img.get('src', '')
                fig_id = re.sub(r'^\./|\.[a-zA-Z]+$', '', img_src)
                content_plan["metadata"]["figures"].append({
                    "fig_id": fig_id,
                    "description": img.get('data-semantic', ''), # 增加语义信息逻辑
                    "figure_width": int(re.search(r'width:\s*(\d+)', img.get('style', '')).group(1)) if "width" in img.get('style', '') else 0,
                    "figure_height": int(re.search(r'height:\s*(\d+)', img.get('style', '')).group(1)) if "height" in img.get('style', '') else 0
                })

    # 3. 提取 Sections (保持之前的逻辑并优化)
    layout_blocks = soup.find_all(class_='layout-block')
    for block in layout_blocks:
        section_data = {
            "id": block.get('data-section-id', 'unknown'),
            "title": "",
            "content": [],
            "tables": [],
            "figures": []
        }
        
        # 提取 Section 标题
        header_el = block.find(class_='section-header')
        if header_el:
            section_data["title"] = header_el.get_text(strip=True)
        
        # 提取内容、图表、表格
        for child in block.find_all(['p', 'ul', 'div'], recursive=False):
            cls = child.get('class', [])
            
            if 'text-block' in cls or 'references-text' in cls:
                p_tags = child.find_all('p')
                if p_tags:
                    section_data["content"].extend([p.get_text(strip=True) for p in p_tags])
                else:
                    section_data["content"].append(child.get_text(strip=True))
            
            elif child.name == 'ul':
                section_data["content"].extend([li.get_text(strip=True) for li in child.find_all('li')])
            
            # 处理嵌套的图表容器
            elif 'figure-container' in cls or 'row-container' in cls:
                imgs = child.find_all('img')
                for img in imgs:
                    src = img.get('src', '')
                    fid = re.sub(r'^\./|\.[a-zA-Z]+$', '', src)
                    style = img.get('style', '')
                    w = int(re.search(r'width:\s*(\d+)', style).group(1)) if "width" in style else 0
                    h = int(re.search(r'height:\s*(\d+)', style).group(1)) if "height" in style else 0
                    
                    # 增加语义信息逻辑
                    semantic_description = img.get('data-semantic', '')
                    
                    item = {"id": fid, "width": w, "height": h, "caption": [], "description": semantic_description}
                    
                    if 'table' in fid.lower():
                        section_data["tables"].append({
                            "table_id": item["id"], 
                            "description": item["description"], # 写入语义字段
                            "table_width": item["width"], 
                            "table_height": item["height"], 
                            "table_caption": []
                        })
                    else:
                        section_data["figures"].append({
                            "fig_id": item["id"], 
                            "description": item["description"], # 写入语义字段
                            "figure_width": item["width"], 
                            "figure_height": item["height"], 
                            "figure_caption": []
                        })

        content_plan["sections"].append(section_data)

    return content_plan


if __name__=="__main__":
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Poster Layout - Graph Edit Networks</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: #f0f0f0;
        }
        #poster-canvas {
            width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }
        header {
            display: flex;
            flex-direction: column;
            margin-bottom: 30px;
        }
        .poster-title {
            font-size: 48px;
            font-weight: bold;
            margin: 0 0 10px 0;
            color: #333;
        }
        .poster-authors {
            font-size: 20px;
            color: #555;
            margin: 0 0 20px 0;
        }
        .header-logos {
            display: flex;
            align-items: center;
            gap: 30px;
            font-size: 14px;
            color: #666;
        }
        main {
            display: flex;
            gap: 30px;
        }
        .column {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        .layout-block {
            display: flex;
            flex-direction: column;
        }
        .section-header {
            background-color: #b05044;
            color: white;
            padding: 8px 15px;
            font-size: 22px;
            margin: 0 0 15px 0;
            border-radius: 2px;
        }
        .text-block {
            font-size: 14px;
            line-height: 1.5;
            margin: 0 0 15px 0;
            color: #333;
            text-align: justify;
        }
        .list-item {
            font-size: 14px;
            margin-bottom: 8px;
            color: #333;
        }
        .figure-container, .row-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 10px 0;
            gap: 10px;
        }
        .row-container {
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-start;
        }
        .references-text {
            font-size: 11px;
            line-height: 1.3;
            color: #444;
        }
        img {
            max-width: 100%;
            height: auto;
            object-fit: contain;
        }
        .highlight-text {
            color: #b05044;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="poster-canvas">
        <header>
            <h1 class="poster-title">[Re] Graph Edit Networks</h1>
            <p class="poster-authors">Vid Stropnik, Maruša Oražem</p>
            <div class="header-logos">
                <div>University of Ljubljana, Faculty of Computer and Information Science</div>
                <div>Data Science @ UL-FRI</div>
                <div>Neural Information Processing Systems</div>
                <div>github.com/vstropnik/re-gen</div>
                <img src="./logo_uni.png" style="width: 60px; height: 60px;" data-semantic="University Logo">
                <img src="./logo_ds.png" style="width: 120px; height: 40px;" data-semantic="Data Science Lab Logo">
            </div>
        </header>

        <main>
            <!-- Column 1 -->
            <div class="column">
                <section class="layout-block" data-section-id="section_1">
                    <h2 class="section-header">Reproduced: Paaßen et. al. (ICLR, 2021)</h2>
                    <p class="text-block">
                        The reproduced paper [bpa21] proposes a novel output layer for graph neural networks (GNNs), the graph edit network called (GEN). This layer yields a sequence of graph edits: node insertions, node deletions, node replacements, edge insertions and edge deletions.
                    </p>
                    <div class="figure-container">
                        <img src="./fig_1.jpg" style="width: 350px; height: 70px;" data-semantic="GEN model architecture showing original graph to predicted graph transformation">
                    </div>
                    <p class="text-block">
                        The authors empirically underpin their theoretical claims about GENs by showing that they perform well in a series of graph time-series prediction tests.
                    </p>
                </section>

                <section class="layout-block" data-section-id="section_2">
                    <h2 class="section-header">DGPs & Tests</h2>
                    <p class="text-block">
                        The paper evaluated several key claims on synthetic datasets, generated with data generating rules, interpreted in the following figures.
                    </p>
                    <div class="figure-container">
                        <img src="./fig_2.jpg" style="width: 350px; height: 52px;" data-semantic="Graph cycles transformation sequence">
                        <img src="./fig_3.jpg" style="width: 350px; height: 94px;" data-semantic="Degree rules for node and edge insertions">
                        <img src="./fig_4.jpg" style="width: 250px; height: 57px;" data-semantic="Conway's Game of Life grid sequence">
                    </div>
                </section>
            </div>

            <!-- Column 2 -->
            <div class="column">
                <section class="layout-block" data-section-id="section_3">
                    <div class="figure-container">
                        <img src="./fig_5.jpg" style="width: 360px; height: 82px;" data-semantic="Boolean Formulae simplification tree sequence">
                        <img src="./fig_6.jpg" style="width: 320px; height: 57px;" data-semantic="Peano Addition modelling addition problems via trees">
                    </div>
                </section>

                <section class="layout-block" data-section-id="section_4">
                    <h2 class="section-header">[Re] Original experimental claims</h2>
                    <p class="text-block">
                        [bpa21] makes three experimental conclusions based on a series of experiments. Symbols below denote a successful reproduction of results.
                    </p>
                    <ul>
                        <li class="list-item">✓ GENs outperform baselines (Variational Graph Autoencoders [KW16] & Variational Graph Recurrent nets [HHN19]) on time-series prediction tasks.</li>
                        <li class="list-item">✓ GENs achieve 100% accuracy on time-series prediction tasks on graphs, generated from Boolean Formulae & Peano Addition DGPs.</li>
                        <li class="list-item">? The runtime of forward passes of a GEN scales sub-quadratically as the number of nodes in a graph increases.</li>
                    </ul>
                    <div class="figure-container">
                        <img src="./fig_7.jpg" style="width: 360px; height: 120px;" data-semantic="Runtime of forward and backward passes vs graph node count">
                    </div>
                    <div class="row-container">
                        <div class="figure-container">
                            <img src="./table_2.png" style="width: 180px; height: 120px;" data-semantic="Log-log linear slope fit for runtime scaling">
                        </div>
                        <div class="figure-container">
                            <img src="./fig_8.jpg" style="width: 170px; height: 90px;" data-semantic="Training loss over iterations for different parameters">
                        </div>
                    </div>
                </section>
            </div>

            <!-- Column 3 -->
            <div class="column">
                <section class="layout-block" data-section-id="section_5">
                    <h2 class="section-header">Improving the experimental setup</h2>
                    <p class="text-block">
                        The facts that graph-to-graph transitions are deterministic and that the space of unique graphs that may be generated by the DGPs is limited, arose some concern about the experimental setup.
                    </p>
                    <div class="figure-container">
                        <img src="./table_3.png" style="width: 350px; height: 53px;" data-semantic="Number of unique graphs generated by different DGPs">
                    </div>
                    <ul>
                        <li class="list-item">Increased cardinality of test time series (5 -> 100)</li>
                        <li class="list-item">Ensured no duplicates between train & test set</li>
                        <li class="list-item">Used established random graph generation methods</li>
                    </ul>
                    <p class="text-block highlight-text">
                        Results were generally worse, but still within a reasonable margin of error.
                    </p>
                    <div class="row-container">
                        <img src="./fig_9.jpg" style="width: 180px; height: 120px;" data-semantic="Distribution of sampled TS lengths for boolean and peano">
                        <img src="./table_1.png" style="width: 160px; height: 90px;" data-semantic="Probability of sampling unique and simplifyable trees">
                    </div>
                </section>

                <section class="layout-block" data-section-id="section_6">
                    <h2 class="section-header">Concluding reproduction notes</h2>
                    <p class="text-block">
                        Our experimental results conclusively show that most of the claims in the original work hold. However, our work beyond the original paper emphasizes the need to pay attention to the experimental setup.
                    </p>
                </section>

                <section class="layout-block" data-section-id="section_7">
                    <h2 class="section-header">References</h2>
                    <div class="references-text">
                        <p>[bpa21] Paaßen, Benjamin, et al. "Graph edit networks." ICLR 2021.</p>
                        <p>[Gar70] Martin Gardner. "The fantastic combinations of John Conway's new solitaire game of life." 1970.</p>
                        <p>[KW16] Thomas N. Kipf and Max Welling. "Variational graph auto-encoders." 2016.</p>
                        <p>[HHN19] Hajiramezanali, Ehsan, et. al. "Variational graph recurrent neural networks." NeurIPS 2019.</p>
                    </div>
                    <div class="figure-container" style="align-self: flex-end;">
                        <img src="./qr_code.png" style="width: 80px; height: 80px;" data-semantic="QR code for the project repository">
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
"""
    content_plan = html_to_content_plan(html_content)
    save_json(content_plan,'./test3.json')
    #with open('./test3.json','w',encoding='utf-8') as f:
        