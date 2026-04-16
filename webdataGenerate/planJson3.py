import os
import json
import re
from bs4 import BeautifulSoup, Tag

# ─────────────────────────────────────────────────────────────────────────────
# 内部工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _clean_text(text: str) -> str:
    """折叠空白字符，返回干净字符串。"""
    return re.sub(r"\s+", " ", text or "").strip()


def _get_fig_id(img_tag: Tag) -> str:
    """优先取 data-fig-id；否则从 src 文件名推断。"""
    fid = img_tag.get("data-fig-id", "")
    if not fid:
        src = img_tag.get("src", "")
        fid = os.path.splitext(os.path.basename(src))[0]
    return fid


def _is_table_img(img_tag: Tag) -> bool:
    """判断是否为表格图：通过 data-fig-id、src 或父容器 data-type。"""
    fid = img_tag.get("data-fig-id", "")
    src = os.path.basename(img_tag.get("src", ""))
    
    # 检查父容器是否有 data-type="table"
    parent_type = ""
    p = img_tag.parent
    while p and p.name != "section":
        if p.get("data-type"):
            parent_type = p.get("data-type")
            break
        p = p.parent

    return fid.startswith("table_") or src.startswith("table_") or parent_type == "table"


def _make_figure_entry(img_tag: Tag, caption_texts: list | None = None) -> dict:
    return {
        "fig_id":         _get_fig_id(img_tag),
        "description":    _clean_text(img_tag.get("alt", "")),
        "img_path":       img_tag.get("src", ""),
        "figure_width":   0,
        "figure_height":  0,
        "figure_caption": caption_texts or [],
    }


def _make_table_entry(img_tag: Tag, caption_texts: list | None = None) -> dict:
    return {
        "table_id":      _get_fig_id(img_tag),
        "description":   _clean_text(img_tag.get("alt", "")),
        "img_path":      img_tag.get("src", ""),
        "table_width":   0,
        "table_height":  0,
        "table_caption": caption_texts or [],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 各区块解析逻辑
# ─────────────────────────────────────────────────────────────────────────────

def _parse_metadata(header_tag: Tag) -> dict:
    """解析 <header data-type="metadata">。"""
    meta = {
        "title":         "",
        "authors":       [],
        "organizations": [],
        "contents":      [],
        "github":        "",
        "figures":       [],
    }

    # 1. Title
    h1 = header_tag.find("h1")
    if h1:
        meta["title"] = _clean_text(h1.get_text())

    # 2. Authors (基于 span 列表)
    auth_container = header_tag.find(attrs={"data-type": "authors"})
    if auth_container:
        meta["authors"] = [_clean_text(s.get_text()) for s in auth_container.find_all("span") if s.get_text().strip()]

    # 3. Organizations
    org_container = header_tag.find(attrs={"data-type": "organizations"})
    if org_container:
        # 提取内部所有文本段落
        meta["organizations"] = [_clean_text(p.get_text()) for p in org_container.find_all(["p", "div", "span"]) if p.get_text().strip()]
        if not meta["organizations"]: # 兜底直接取文本
            meta["organizations"] = [_clean_text(org_container.get_text())]

    # 4. GitHub / Nav Links
    nav = header_tag.find("nav")
    if nav:
        for a in nav.find_all("a"):
            href = a.get("href", "")
            if "github" in href.lower() or "github" in a.get_text().lower():
                meta["github"] = href

    # 5. Figures in Metadata
    for img in header_tag.find_all("img"):
        meta["figures"].append(_make_figure_entry(img))

    # 6. Contents (描述性文本：排除已提取的 title, authors, orgs)
    for p in header_tag.find_all("p"):
        if p.get("data-type") in ["authors", "organizations"]:
            continue
        txt = _clean_text(p.get_text())
        if txt:
            meta["contents"].append(txt)

    return meta


def _collect_content(tag: Tag, section: dict, visited_imgs: set):
    """深度优先遍历，解析正文、图表容器、组图和代码块。"""
    for child in tag.children:
        if not isinstance(child, Tag):
            continue

        tag_name = child.name.lower()
        dtype = child.get("data-type")

        # A. 跳过已提取的标题
        if tag_name == "h2":
            continue

        # B. 处理图表容器 (figure / table)
        if tag_name == "div" and dtype in ("figure", "table"):
            cap_tag = child.find(attrs={"data-type": "caption"})
            caption = [_clean_text(cap_tag.get_text())] if cap_tag else []
            
            imgs = child.find_all("img")
            for img in imgs:
                src = img.get("src", "")
                if src not in visited_imgs:
                    visited_imgs.add(src)
                    if _is_table_img(img) or dtype == "table":
                        section["tables"].append(_make_table_entry(img, caption))
                    else:
                        section["figures"].append(_make_figure_entry(img, caption))
            continue

        # C. 处理并排组图 (figure-group)
        if tag_name == "div" and dtype == "figure-group":
            imgs = child.find_all("img")
            # 尝试寻找紧随其后的 caption-group
            cap_group = child.find_next_sibling(attrs={"data-type": "caption-group"})
            caps = cap_group.find_all(attrs={"data-type": "caption-item"}) if cap_group else []
            
            for i, img in enumerate(imgs):
                src = img.get("src", "")
                if src not in visited_imgs:
                    visited_imgs.add(src)
                    current_cap = [_clean_text(caps[i].get_text())] if i < len(caps) else []
                    if _is_table_img(img):
                        section["tables"].append(_make_table_entry(img, current_cap))
                    else:
                        section["figures"].append(_make_figure_entry(img, current_cap))
            continue

        # D. 处理文本及代码块 (p, h3-h6, pre)
        if tag_name in ("p", "h3", "h4", "h5", "h6", "pre"):
            if dtype == "caption" or dtype == "caption-item":
                continue  # 标题已在容器逻辑中处理
            
            if tag_name == "pre":
                txt = child.get_text().strip() # 保护代码换行
            else:
                txt = _clean_text(child.get_text())
            
            if txt:
                section["content"].append(txt)
            continue

        # E. 处理列表
        if tag_name == "ul":
            for li in child.find_all("li", recursive=False):
                txt = _clean_text(li.get_text())
                if txt:
                    section["content"].append(txt)
            continue

        # F. 递归处理
        _collect_content(child, section, visited_imgs)


def _parse_section(section_tag: Tag) -> dict:
    """解析 <section data-type="section">。"""
    section = {
        "id":      section_tag.get("id", ""),
        "title":   "",
        "content": [],
        "figures": [],
        "tables":  [],
    }
    h2 = section_tag.find("h2")
    if h2:
        section["title"] = _clean_text(h2.get_text())
    
    _collect_content(section_tag, section, visited_imgs=set())
    return section


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口
# ─────────────────────────────────────────────────────────────────────────────

def parse_html_to_content_plan(html_path: str, output_dir: str) -> str:
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    plan = {"metadata": {}, "sections": []}

    # 1. Metadata
    header = soup.find("header", attrs={"data-type": "metadata"})
    if header:
        plan["metadata"] = _parse_metadata(header)
    else:
        # 兼容性兜底
        title_tag = soup.find("title")
        plan["metadata"] = {
            "title": _clean_text(title_tag.get_text()) if title_tag else "",
            "authors": [], "organizations": [], "contents": [], "github": "", "figures": []
        }

    # 2. Sections (统一由 data-type="section" 驱动)
    for sec in soup.find_all("section", attrs={"data-type": "section"}):
        plan["sections"].append(_parse_section(sec))

    # 3. 输出保存
    html_stem = os.path.splitext(os.path.basename(html_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, html_stem + ".json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    return out_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python html_to_content_plan.py <input.html> <output_dir>")
        sys.exit(1)
    result_path = parse_html_to_content_plan(sys.argv[1], sys.argv[2])
    print(f"✅ Generated: {result_path}")