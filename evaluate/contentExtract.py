"""
html_to_content_plan.py
-----------------------
将手动编码的 poster HTML 文件解析为 content_plan.json。

对外接口：
    parse_html_to_content_plan(html_path, output_dir) -> str
        html_path  : HTML 文件路径
        output_dir : 输出目录；JSON 文件名与 HTML 同名（扩展名替换为 .json）
        返回值     : 生成的 JSON 文件完整路径

解析规则：
  - <header data-type="metadata">   → metadata（title / authors / organizations / figures）
  - <section data-type="section">   → sections[]（id / title / content / figures / tables）
  - <section data-type="reference"> → sections[]（title="References"，content 存文献条目）
  - <img data-fig-id="table_*"> 或 src="./table_*.jpg"  → tables[]
  - <img src="./equations_*.jpg">   → figures[]（公式图与普通图统一归入 figures）
  - figure_width / figure_height / table_width / table_height → 0（HTML 中无尺寸信息）
  - figure_caption / table_caption  → <figcaption> 文本，无则 []
"""

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
    """优先取 data-fig-id；否则从 src 文件名推断（去掉扩展名）。"""
    fid = img_tag.get("data-fig-id", "")
    if not fid:
        src = img_tag.get("src", "")
        fid = os.path.splitext(os.path.basename(src))[0]
    return fid


def _is_table_img(img_tag: Tag) -> bool:
    """data-fig-id 或 src 文件名以 'table_' 开头则视为 table。"""
    fid = img_tag.get("data-fig-id", "")
    src = os.path.basename(img_tag.get("src", ""))
    return fid.startswith("table_") or src.startswith("table_")


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


def _find_caption(img_tag: Tag) -> list:
    """在 img 父节点内查找 <figcaption>，返回文本列表（0 或 1 项）。"""
    parent = img_tag.parent
    if parent is None:
        return []
    figcap = parent.find("figcaption")
    if figcap:
        txt = _clean_text(figcap.get_text())
        return [txt] if txt else []
    return []


# ─────────────────────────────────────────────────────────────────────────────
# 各区块解析
# ─────────────────────────────────────────────────────────────────────────────

def _parse_metadata(header_tag: Tag) -> dict:
    """解析 <header data-type="metadata"> 块。"""
    meta = {
        "title":         "",
        "authors":       [],
        "organizations": [],
        "github":        "",
        "figures":       [],
    }

    h1 = header_tag.find("h1")
    if h1:
        meta["title"] = _clean_text(h1.get_text())

    author_div = header_tag.find("div", class_=re.compile(r"text-xl|text-2xl"))
    if author_div:
        raw = _clean_text(author_div.get_text())
        meta["authors"] = [a.strip().rstrip("*") for a in raw.split(",") if a.strip()]

    org_div = header_tag.find("div", class_=re.compile(r"text-gray"))
    if org_div:
        raw = _clean_text(org_div.get_text())
        meta["organizations"] = [o.strip() for o in raw.split(",") if o.strip()]

    for a_tag in header_tag.find_all("a"):
        href = a_tag.get("href", "")
        if "github" in href.lower():
            meta["github"] = href
            break

    for img in header_tag.find_all("img"):
        meta["figures"].append(_make_figure_entry(img))

    return meta


def _collect_content(tag: Tag, section: dict, visited_imgs: set):
    """
    深度优先遍历 tag，将内容分类填入 section：
      - 文本（p / h3-h6 / li） → section["content"]
      - 普通图 / 公式图        → section["figures"]
      - table 图               → section["tables"]
    """
    for child in tag.children:
        if not isinstance(child, Tag):
            continue

        tag_name = child.name.lower()

        # 跳过 section 标题（已单独提取）
        if tag_name == "h2":
            continue

        # 段落 / 小标题
        if tag_name in ("p", "h3", "h4", "h5", "h6"):
            if "hidden" in child.get("class", []):   # LaTeX 备注行，跳过
                continue
            txt = _clean_text(child.get_text())
            if txt:
                section["content"].append(txt)
            continue

        # 无序列表：每个 <li> 作为独立 content 条目
        if tag_name == "ul":
            for li in child.find_all("li", recursive=False):
                txt = _clean_text(li.get_text())
                if txt:
                    section["content"].append(txt)
            continue

        # 裸 <img>
        if tag_name == "img":
            src = child.get("src", "")
            if src in visited_imgs:
                continue
            visited_imgs.add(src)
            cap = _find_caption(child)
            if _is_table_img(child):
                section["tables"].append(_make_table_entry(child, cap))
            else:
                section["figures"].append(_make_figure_entry(child, cap))
            continue

        # <figure> 包裹的图片
        if tag_name == "figure":
            img = child.find("img")
            if img:
                src = img.get("src", "")
                if src not in visited_imgs:
                    visited_imgs.add(src)
                    figcap = child.find("figcaption")
                    cap = [_clean_text(figcap.get_text())] if figcap else []
                    if _is_table_img(img):
                        section["tables"].append(_make_table_entry(img, cap))
                    else:
                        section["figures"].append(_make_figure_entry(img, cap))
            continue

        # 其他容器：递归
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


def _parse_reference_section(section_tag: Tag) -> dict:
    """解析 <section data-type="reference">，每条 <li> 作为 content 条目。"""
    section = {
        "id":      section_tag.get("id", "section_ref"),
        "title":   "",
        "content": [],
        "figures": [],
        "tables":  [],
    }
    h2 = section_tag.find("h2")
    if h2:
        section["title"] = _clean_text(h2.get_text())
    for li in section_tag.find_all("li"):
        txt = _clean_text(li.get_text())
        if txt:
            section["content"].append(txt)
    return section


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口
# ─────────────────────────────────────────────────────────────────────────────

def parse_html_to_content_plan(html_path: str, output_dir: str) -> str:
    """
    将 poster HTML 文件解析为 content_plan.json 并保存。

    参数
    ----
    html_path  : str — HTML 文件的完整路径
    output_dir : str — 输出目录；若不存在则自动创建

    返回
    ----
    str — 生成的 JSON 文件完整路径
    """
    # ── 读取并解析 HTML ───────────────────────────────────────────────────────
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    plan = {"metadata": {}, "sections": []}

    # metadata
    header = soup.find(lambda t: t.name == "header" and t.get("data-type") == "metadata")
    if header:
        plan["metadata"] = _parse_metadata(header)
    else:
        title_tag = soup.find("title")
        plan["metadata"] = {
            "title":         _clean_text(title_tag.get_text()) if title_tag else "",
            "authors":       [],
            "organizations": [],
            "github":        "",
            "figures":       [],
        }

    # sections
    for sec in soup.find_all("section", attrs={"data-type": True}):
        dtype = sec.get("data-type", "")
        if dtype == "section":
            plan["sections"].append(_parse_section(sec))
        elif dtype == "reference":
            plan["sections"].append(_parse_reference_section(sec))

    # ── 确定输出路径 ──────────────────────────────────────────────────────────
    html_stem = os.path.splitext(os.path.basename(html_path))[0]  # 去掉 .html
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir,   "htmlContentExtract.json")

    # ── 写入 JSON ─────────────────────────────────────────────────────────────
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# 命令行入口（可选）
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python html_to_content_plan.py <input.html> <output_dir>")
        sys.exit(1)

    result_path = parse_html_to_content_plan(sys.argv[1], sys.argv[2])
    print(f"✅  已生成: {result_path}")