import os
import random
from bs4 import BeautifulSoup

# =========================
# 负样本函数定义
# =========================

def add_fake_section(html):
    fake_section = """
    <section id="section_fake">
        <h2>Fake Section</h2>
        <p>Fake content not in JSON.</p>
    </section>
    """
    return html.replace("</body>", fake_section + "\n</body>"), "新增不存在的section（捏造内容）"


def add_fake_figure(html):
    fake_fig = """
    <img src="log.jpg">
    <p class="caption">Fake figure</p>
    """
    return html.replace("</section>", fake_fig + "\n</section>", 1), "新增不存在的图像（捏造内容）"


def move_figure_to_wrong_section(html):
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    figs = soup.find_all("img")

    if len(sections) < 2 or not figs:
        return html, None

    fig = random.choice(figs)
    fig.extract()

    target_section = random.choice(sections)
    target_section.append(fig)

    return str(soup), "图像位置错误（跨section错位）"


def modify_caption(html):
    soup = BeautifulSoup(html, "html.parser")
    captions = soup.find_all("p", {"class": "caption"})

    if not captions:
        return html, None

    cap = random.choice(captions)
    cap.string = "This figure shows experimental results."

    return str(soup), "caption被修改（未保持原文）"


def remove_random_figure(html):
    soup = BeautifulSoup(html, "html.parser")
    figs = soup.find_all("img")

    if not figs:
        return html, None

    random.choice(figs).extract()

    return str(soup), "图像内容缺失（遗漏figure）"


def remove_section(html):
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")

    if len(sections) <= 1:
        return html, None

    random.choice(sections).extract()

    return str(soup), "章节缺失（遗漏section）"


def duplicate_paragraph(html):
    soup = BeautifulSoup(html, "html.parser")
    ps = soup.find_all("p")

    if not ps:
        return html, None

    p = random.choice(ps)
    new_p = soup.new_tag("p")
    new_p.string = p.text
    p.insert_after(new_p)

    return str(soup), "文本重复（生成冗余内容）"


# 所有负样本函数池
NEGATIVE_FUNCTIONS = [
    add_fake_section,
    add_fake_figure,
    move_figure_to_wrong_section,
    modify_caption,
    remove_random_figure,
    remove_section,
    duplicate_paragraph
]


# =========================
# 主函数
# =========================

def generate_negative_dataset(
    dataset_path,
    sample_ratio=0.3,
    num_funcs_range=(1, 3)
):
    """
    dataset_path: 数据集路径
    sample_ratio: 采样比例（0~1）
    num_funcs_range: 每条数据叠加的负样本函数数量范围 (min, max)
    """

    folders = [
        os.path.join(dataset_path, d)
        for d in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, d))
    ]

    sampled_folders = random.sample(
        folders,
        max(1, int(len(folders) * sample_ratio))
    )

    print(f"采样 {len(sampled_folders)} / {len(folders)} 个数据")

    for folder in sampled_folders:
        html_path = os.path.join(folder, "poster.html")

        if not os.path.exists(html_path):
            continue

        # 读取HTML
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        new_html = html
        reasons = []

        # 随机选择函数数量
        n_funcs = random.randint(num_funcs_range[0], num_funcs_range[1])
        funcs = random.sample(NEGATIVE_FUNCTIONS, n_funcs)

        for func in funcs:
            new_html, reason = func(new_html)
            if reason:
                reasons.append(reason)

        # 保存 negative html
        neg_html_path = os.path.join(folder, "negative_poster.html")
        with open(neg_html_path, "w", encoding="utf-8") as f:
            f.write(new_html)

        # 保存原因
        reason_path = os.path.join(folder, "negative_reason.txt")
        with open(reason_path, "w", encoding="utf-8") as f:
            for r in reasons:
                f.write(r + "\n")

    print("负样本生成完成 ✅")

if __name__ == "__main__":
    generate_negative_dataset(
        dataset_path="../finetuneData/web/pair_data2",
        sample_ratio=0.3,
        num_funcs_range=(1, 3)
    )