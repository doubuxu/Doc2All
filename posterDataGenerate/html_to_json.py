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
                    
                    item = {"id": fid, "width": w, "height": h, "caption": []}
                    
                    if 'table' in fid.lower():
                        section_data["tables"].append({
                            "table_id": item["id"], 
                            "table_width": item["width"], 
                            "table_height": item["height"], 
                            "table_caption": []
                        })
                    else:
                        section_data["figures"].append({
                            "fig_id": item["id"], 
                            "figure_width": item["width"], 
                            "figure_height": item["height"], 
                            "figure_caption": []
                        })

        content_plan["sections"].append(section_data)

    return content_plan

# 执行转换并打印完整 JSON
# result = html_to_content_plan_refined(your_html_string)
# print(json.dumps(result, indent=2, ensure_ascii=False))

# 测试使用
# html_str = """ ... 你的 HTML 代码 ... """
# plan = html_to_content_plan(html_str)
# print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__=="__main__":
    html_code="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Academic Poster Layout</title>
    <style>
        /* 全局容器：固定宽高，严格参考海报比例 */
        #poster-canvas {
            width: 3200px;
            height: 2200px;
            display: flex;
            flex-direction: column;
            padding: 60px;
            box-sizing: border-box;
            font-family: "Arial", sans-serif;
            line-height: 1.4;
            overflow: hidden;
        }

        /* 头部区域 */
        header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 40px;
            width: 100%;
        }

        .header-left {
            display: flex;
            flex-direction: column;
        }

        .poster-title {
            font-size: 84px;
            font-weight: bold;
            margin: 0;
        }

        .poster-authors {
            font-size: 32px;
            margin-top: 20px;
        }

        .header-logos {
            display: flex;
            gap: 40px;
            align-items: center;
        }

        /* 主体多栏架构 */
        main {
            display: flex;
            flex-direction: row;
            gap: 60px;
            flex: 1;
        }

        .column {
            display: flex;
            flex-direction: column;
            flex: 1;
            gap: 30px;
        }

        /* 逻辑区块 */
        .layout-block {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .section-header {
            font-size: 42px;
            font-weight: bold;
            margin: 0;
            padding: 10px 20px;
            text-transform: none;
        }

        .text-block {
            font-size: 26px;
            margin: 0;
            text-align: justify;
        }

        .list-item {
            font-size: 26px;
            margin-bottom: 10px;
        }

        /* 图表载体 */
        .figure-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }

        .row-container {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }

        img {
            object-fit: contain;
        }

        /* 引用文献专用 */
        .references-text {
            font-size: 18px;
            line-height: 1.2;
        }
    </style>
</head>
<body>
    <div id="poster-canvas">
        <header>
            <div class="header-left">
                <h1 class="poster-title">[Re] Graph Edit Networks</h1>
                <p class="poster-authors">Vid Stropnik, Maruša Oražem</p>
            </div>
            <div class="header-logos">
                <!-- 占位符，实际使用时替换为对应Logo -->
                <div style="width: 200px; height: 100px;">Data Science @ UL-FRI</div>
                <div style="width: 300px; height: 100px;">University of Ljubljana</div>
                <div style="width: 200px; height: 100px;">NeurIPS</div>
            </div>
        </header>

        <main>
            <!-- 第一列 -->
            <div class="column" style="flex: 0 0 1000px;">
                <section class="layout-block" data-section-id="section_1">
                    <h2 class="section-header">Reproduced: Paaßen et. al. (ICLR, 2021)</h2>
                    <p class="text-block">
                        The reproduced paper [bpa21] proposes a novel output layer for graph neural networks (GNNs), the graph edit network called (GEN). This layer yields a sequence of graph edits: node insertions, node deletions, node replacements, edge insertions and edge deletions. These finite sequences of edits, also referred to as edit scripts are general enough to describe any graph-to-graph transformation and are not only very interpretable for humans, but also computationally efficient. These properties establish GENs as a useful tool for work in the domain of graph time series prediction under the Markovian assumption.
                    </p>
                    <div class="figure-container">
                        <img src="./fig_1.jpg" style="width: 958px; height: 192px;" alt="GEN Architecture">
                    </div>
                    <p class="text-block">
                        The authors empirically underpin their theoretical claims about GENs by showing that they perform well in a series of graph time-series prediction tests. They define several data generating processes (DGPs), from which the GEN attempts to learn the user-defined mapping functions. Our work reproduces these experiments and evaluates the suitability of the DGPs for the conclusions made in the original paper.
                    </p>
                </section>

                <section class="layout-block" data-section-id="section_2">
                    <h2 class="section-header">DGPs & Tests</h2>
                    <p class="text-block">
                        The paper evaluated several key claims on synthetic datasets, generated with data generating rules, interpreted in the following figures.
                    </p>
                    <div class="figure-container">
                        <img src="./fig_2.jpg" style="width: 980px; height: 145px;" alt="Graph cycles">
                    </div>
                    <div class="figure-container">
                        <img src="./fig_3.jpg" style="width: 980px; height: 262px;" alt="Degree rules">
                    </div>
                    <div class="figure-container">
                        <img src="./fig_4.jpg" style="width: 699px; height: 159px;" alt="Conway's Game of Life">
                    </div>
                </section>
            </div>

            <!-- 第二列 -->
            <div class="column" style="flex: 0 0 1000px;">
                <div class="figure-container">
                    <img src="./fig_5.jpg" style="width: 1012px; height: 230px;" alt="Boolean Formulae">
                </div>
                <div class="figure-container">
                    <img src="./fig_6.jpg" style="width: 908px; height: 161px;" alt="Peano Addition">
                </div>

                <section class="layout-block" data-section-id="section_3">
                    <h2 class="section-header">[Re] Original experimental claims</h2>
                    <p class="text-block">[bpa21] makes three experimental conclusions based on a series of experiments. ✓ symbols below denote a successful reproduction of results.</p>
                    <ul>
                        <li class="list-item">✓ GENs outperform baselines (Variational Graph Autoencoders [KW16] & Variational Graph Recurrent nets [HHN19]) on time-series prediction tasks, generated from Graph Cycles, Degree Rules & Game of Life DGPs.</li>
                        <li class="list-item">✓ GENs achieve 100% accuracy on time-series prediction tasks on graphs, generated from Boolean Formulae & Peano Addition DGPs.</li>
                        <li class="list-item">? The runtime of forward passes of a GEN scales sub-quadratically as the number of nodes in a graph increases. The runtime of training back-passes scales approximately linearly.</li>
                    </ul>
                    <div class="figure-container">
                        <img src="./fig_7.jpg" style="width: 990px; height: 330px;" alt="Runtime plots">
                    </div>
                    <div class="row-container">
                        <div class="figure-container">
                            <img src="./table_1.jpg" style="width: 455px; height: 252px;" alt="Runtime slope fit table">
                        </div>
                        <div class="figure-container">
                            <img src="./fig_8.jpg" style="width: 473px; height: 253px;" alt="Loss plot">
                        </div>
                    </div>
                    <div class="row-container">
                        <p class="text-block" style="font-size: 18px; width: 450px;">The runtime scaling evaluation was carried out on the ArXiv citation network [LKF05] with the graph variants generated by a different number of months considered.</p>
                        <p class="text-block" style="font-size: 18px; width: 450px;">While the focus here is speed, we have to note that the experiment in the original paper fails to optimize the criterion loss, thus casting doubt on the results.</p>
                    </div>
                </section>
            </div>

            <!-- 第三列 -->
            <div class="column" style="flex: 0 0 1000px;">
                <section class="layout-block" data-section-id="section_4">
                    <h2 class="section-header">Improving the experimental setup</h2>
                    <p class="text-block">
                        The facts that graph-to-graph transitions are deterministic and that the space of unique graphs that may be generated by the DGPs is limited (as shown in the table below), arose some concern about the experimental setup: Does the solver generalize, or does it simply memorize the graph-to-graph transitions?
                    </p>
                    <div class="figure-container">
                        <img src="./table_2.jpg" style="width: 960px; height: 145px;" alt="Unique graphs table">
                    </div>
                    <p class="text-block">We reproduced the claims (1) and (2) with the following adjustments:</p>
                    <ul>
                        <li class="list-item">Increased cardinality of test time series (5 -> 100)</li>
                        <li class="list-item">Ensured no duplicates between train & test set</li>
                        <li class="list-item">Used established random graph generation methods (ie. Erdős–Rényi)</li>
                    </ul>
                    <p class="text-block">We noticed that most sampled graphs in the tree dynamic graph experiments were un-simplifyable, so constraints were relaxed here.</p>
                    <p class="text-block" style="font-weight: bold;">Results were generally worse, but still within a reasonable margin of error.</p>
                    <div class="figure-container">
                        <img src="./fig_9.jpg" style="width: 948px; height: 334px;" alt="Distribution and Prob table">
                    </div>
                </section>

                <section class="layout-block" data-section-id="section_5">
                    <h2 class="section-header">Concluding reproduction notes</h2>
                    <p class="text-block">
                        Our experimental results conclusively show that most of the claims in the original work hold. However, our work beyond the original paper emphasizes the need to pay attention to the experimental setup, especially when working with synthetically generated data, sampled from functions, rather than gathered from an external system.
                    </p>
                </section>

                <section class="layout-block" data-section-id="section_6">
                    <h2 class="section-header">References</h2>
                    <div class="references-text">
                        <p>[bpa21] Paaßen, Benjamin, et al. "Graph edit networks." In: International Conference on Learning Representations. 2020</p>
                        <p>[Gar70] Martin Gardner. "The fantastic combinations of John Conway's new solitaire game of life." In: Sc. Am., 223:20-123, 1970</p>
                        <p>[KW16] Thomas N. Kipf and Max Welling. "Variational graph auto-encoders" In: Proceedings of the NIPS 2016 Workshop on Bayesian Deep Learning, 2016</p>
                        <p>[HHN19] Hajiramezanali, Ehsan, et. al. "Variational graph recurrent neural networks." In: Proceedings of the 32nd International Conference on Advances in Neural Information Processing Systems (NeurIPS 2019), pp. 10700-10710, 2019</p>
                        <p>[LKF05] Leskovec, Jure, Jon Kleinberg, and Christos Faloutsos. "Graphs over time: densification laws, shrinking diameters and possible explanations." In: Proceedings of the eleventh ACM SIGKDD international conference on Knowledge discovery in data mining. 2005.</p>
                    </div>
                </section>
                
                <!-- QR Code 占位 -->
                <div style="align-self: flex-end; width: 150px; height: 150px; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px;">QR CODE</div>
            </div>
        </main>
    </div>
</body>
</html>
"""
    json_data = html_to_content_plan(html_code)
    save_json(json_data,'test2.json')