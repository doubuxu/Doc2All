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
    """获取图片 ID。优先从 data-fig-id 属性取，否则从 src 文件名推导。"""
    fid = img_tag.get("data-fig-id", "")
    if fid:
        return fid
    src = img_tag.get("src", "")
    if src:
        return os.path.splitext(os.path.basename(src))[0]
    return ""


# ── Tailwind spacing 映射表（rem → px，1rem = 4px） ──
_TAILWIND_SPACING = {
    '0': 0, '0\\.5': 2, '1': 4, '1\\.5': 6, '2': 8, '2\\.5': 10,
    '3': 12, '3\\.5': 14, '4': 16, '5': 20, '6': 24, '7': 28,
    '8': 32, '9': 36, '10': 40, '11': 44, '12': 48, '14': 56,
    '16': 64, '20': 80, '24': 96, '28': 112, '32': 128, '36': 144,
    '40': 160, '44': 176, '48': 192, '52': 208, '56': 224,
    '60': 240, '64': 256, '72': 288, '80': 320, '96': 384,
}

# ── 预编译正则 ──
_RE_H_STD = re.compile(r'\bh-(\d+(?:\.\d+)?)(?!\[)')       # h-40
_RE_W_STD = re.compile(r'\bw-(\d+(?:\.\d+)?)(?!\[)')       # w-60
_RE_H_ARB = re.compile(r'\bh-\[(\d+)px\]')                 # h-[200px]
_RE_W_ARB = re.compile(r'\bw-\[(\d+)px\]')                 # w-[300px]
_RE_STYLE_W = re.compile(r'\bwidth\s*:\s*(\d+)\s*px', re.I) # style="width:300px"
_RE_STYLE_H = re.compile(r'\bheight\s*:\s*(\d+)\s*px', re.I) # style="height:200px"


def _parse_dimensions_from_tag(tag: Tag) -> tuple[int | None, int | None]:
    """从标签及其所有祖先上解析宽高像素值。

    优先级：style 属性 > Tailwind 任意值 h-[Xpx]/w-[Xpx] > Tailwind 标准 h-N/w-N。
    只有两个维度都能解析到时才返回，否则返回 (None, None)。
    """
    height_px = None
    width_px = None

    for t in [tag] + (list(tag.parents) if tag else []):
        if not isinstance(t, Tag):
            continue

        # ── 来源 1：style="width:300px; height:200px" ──
        style = t.get("style") or ""
        if style and (height_px is None or width_px is None):
            if width_px is None:
                m = _RE_STYLE_W.search(style)
                if m:
                    width_px = int(m.group(1))
            if height_px is None:
                m = _RE_STYLE_H.search(style)
                if m:
                    height_px = int(m.group(1))

        # ── 来源 2：class 中的 Tailwind 值 ──
        classes = t.get("class") or []
        cls_str = " ".join(classes)

        if height_px is None:
            m_arb = _RE_H_ARB.search(cls_str)
            if m_arb:
                height_px = int(m_arb.group(1))
            else:
                m_std = _RE_H_STD.search(cls_str)
                if m_std:
                    height_px = _TAILWIND_SPACING.get(m_std.group(1))

        if width_px is None:
            m_arb = _RE_W_ARB.search(cls_str)
            if m_arb:
                width_px = int(m_arb.group(1))
            else:
                m_std = _RE_W_STD.search(cls_str)
                if m_std:
                    width_px = _TAILWIND_SPACING.get(m_std.group(1))

        # 两个维度都解析到就可以提前退出
        if height_px is not None and width_px is not None:
            break

    if height_px is not None and width_px is not None:
        return height_px, width_px
    return None, None


def _is_formula(img_tag: Tag) -> bool:
    """判断是否为公式图片（data-fig-id 以 equation 开头）。"""
    fid = _get_fig_id(img_tag)
    return fid.startswith("equation") if fid else False


def _is_table(img_tag: Tag) -> bool:
    """判断是否为表格图片。"""
    dtype = (img_tag.get("data-type") or "").lower()
    if dtype == "table":
        return True
    fid = _get_fig_id(img_tag)
    if fid and fid.startswith("table_"):
        return True
    src = img_tag.get("src", "")
    if src and os.path.basename(src).startswith("table_"):
        return True
    return False


def _make_figure_entry(img_tag: Tag, caption_list: list | None = None) -> dict:
    h, w = _parse_dimensions_from_tag(img_tag)
    return {
        "fig_id":         _get_fig_id(img_tag),
        "description":    _clean_text(img_tag.get("alt", "")),
        "img_path":       img_tag.get("src", ""),
        "figure_width":   w if w is not None else 0,
        "figure_height":  h if h is not None else 0,
        "figure_caption": caption_list or [],
    }


def _make_table_entry(img_tag: Tag, caption_list: list | None = None) -> dict:
    h, w = _parse_dimensions_from_tag(img_tag)
    return {
        "table_id":      _get_fig_id(img_tag),
        "description":   _clean_text(img_tag.get("alt", "")),
        "img_path":      img_tag.get("src", ""),
        "table_width":   w if w is not None else 0,
        "table_height":  h if h is not None else 0,
        "table_caption": caption_list or [],
    }


def _make_equation_entry(img_tag: Tag, caption_list: list | None = None) -> dict:
    h, w = _parse_dimensions_from_tag(img_tag)
    return {
        "eq_id":       _get_fig_id(img_tag),
        "description": _clean_text(img_tag.get("alt", "")),
        "img_path":    img_tag.get("src", ""),
        "eq_width":    w if w is not None else 0,
        "eq_height":   h if h is not None else 0,
        "eq_caption":  caption_list or [],
    }


def _find_captions_for_img(img_tag: Tag) -> list:
    """为单张 <img> 查找关联的 caption 文本。"""
    captions = []

    # 策略 1：<figure> → <figcaption>
    figure_parent = img_tag.find_parent("figure")
    if figure_parent:
        for fc in figure_parent.find_all("figcaption"):
            txt = _clean_text(fc.get_text())
            if txt and txt not in captions:
                captions.append(txt)

    # 策略 2：data-type="caption"（兼容旧写法）
    if not captions:
        parent = img_tag.parent
        depth = 0
        while parent and depth < 5:
            if isinstance(parent, Tag):
                for cap in parent.find_all(attrs={"data-type": "caption"}):
                    txt = _clean_text(cap.get_text())
                    if txt and txt not in captions:
                        captions.append(txt)
            parent = parent.parent
            depth += 1

    return captions


def _get_text_with_links(tag: Tag) -> str:
    """智能文本提取：含 <a> 时返回 '文本 (URL)' 格式。"""
    if tag.name == "a":
        href = tag.get("href", "")
        text = _clean_text(tag.get_text())
        return f"{text} ({href})" if text and href else (text or href)

    links = tag.find_all("a")
    if links:
        full_text = _clean_text(tag.get_text())
        for link in links:
            href = link.get("href", "")
            link_text = _clean_text(link.get_text())
            if link_text and href:
                full_text = full_text.replace(link_text, f"{link_text} ({href})", 1)
        return full_text

    return _clean_text(tag.get_text())


def _is_inside_figure_or_table_container(tag: Tag) -> bool:
    """判断标签是否在 figure / table 相关容器内部。"""
    for parent in tag.find_parents():
        if isinstance(parent, Tag):
            dt = (parent.get("data-type") or "").lower()
            if dt in ("figure", "table"):
                return True
            if parent.name == "figure":
                return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# 各区块解析逻辑
# ─────────────────────────────────────────────────────────────────────────────

def _parse_metadata(header_tag: Tag) -> dict:
    meta = {
        "title": "", "authors": [], "organizations": [], "github": "",
        "figures": [], "content": []
    }

    # ── 1. 基础信息 ──
    h1 = header_tag.find("h1")
    if h1:
        meta["title"] = _clean_text(h1.get_text())

    auth_div = header_tag.select_one('[data-type="authors"]')
    if auth_div:
        meta["authors"] = [a.strip() for a in _clean_text(auth_div.get_text()).split(",") if a.strip()]

    org_div = header_tag.select_one('[data-type="organizations"]')
    if org_div:
        meta["organizations"] = [o.strip() for o in _clean_text(org_div.get_text()).split(",") if o.strip()]

    # ── 2. 链接 ──
    for a_tag in header_tag.find_all("a"):
        href = a_tag.get("href", "")
        if "github.com" in href.lower() and href.startswith("http"):
            meta["github"] = href

    # ── 3. 图片 ──
    visited_srcs = set()
    for img in header_tag.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        visited_srcs.add(src)
        caps = _find_captions_for_img(img)
        meta["figures"].append(_make_figure_entry(img, caps))

    # ── 4. Content 提取 ──
    excluded_nodes = header_tag.select('h1, [data-type="authors"], [data-type="organizations"]')
    excluded_texts = [_clean_text(n.get_text()) for n in excluded_nodes if _clean_text(n.get_text())]

    for tag in header_tag.find_all(["p", "span", "a"]):
        if tag.get("data-type") in ("authors", "organizations"):
            continue
        if tag.find_parent("figure"):
            continue
        if tag.find(["p", "span", "div", "a"]):
            continue

        raw_txt = tag.get_text(strip=True)
        if not raw_txt:
            continue
        if any(raw_txt in ex for ex in excluded_texts):
            continue

        txt = _get_text_with_links(tag)
        if txt and txt not in meta["content"]:
            meta["content"].append(txt)

    return meta


def _parse_section(section_tag: Tag) -> dict:
    section = {
        "id": "", "title": "", "content": [],
        "figures": [], "tables": [], "equations": []
    }
    section["id"] = section_tag.get("id", "")

    h2 = section_tag.find("h2")
    if h2:
        section["title"] = _clean_text(h2.get_text())

    # ── 1. 图片分类收集 ──
    visited_srcs = set()
    for img in section_tag.find_all("img"):
        src = img.get("src", "")
        if not src or src in visited_srcs:
            continue
        visited_srcs.add(src)

        caps = _find_captions_for_img(img)

        if _is_formula(img):
            section["equations"].append(_make_equation_entry(img, caps))
        elif _is_table(img):
            section["tables"].append(_make_table_entry(img, caps))
        else:
            section["figures"].append(_make_figure_entry(img, caps))

    # ── 2. 文本内容提取 ──
    for tag in section_tag.find_all(["p", "h3", "h4", "h5", "h6", "li", "span", "a"]):
        if tag.name == "figcaption":
            continue
        if (tag.get("data-type") or "").lower() == "caption":
            continue
        if _is_inside_figure_or_table_container(tag):
            continue
        if tag.name == "img":
            continue

        if tag.find(["p", "span", "div", "a"]):
            is_independent_link = (
                tag.name == "a"
                and tag.parent
                and tag.parent.name not in ("p", "li", "span", "figcaption")
            )
            if not is_independent_link:
                continue

        txt = _get_text_with_links(tag)
        txt_stripped = txt.strip()
        if txt_stripped and txt not in section["content"]:
            section["content"].append(txt)

    return section


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口（不修改）
# ─────────────────────────────────────────────────────────────────────────────

def parse_html_to_content_plan(html_path: str, output_dir: str) -> str:
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Missing: {html_path}")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    plan = {"metadata": {}, "sections": []}

    header = soup.find("header", attrs={"data-type": "metadata"})
    if header:
        plan["metadata"] = _parse_metadata(header)

    for sec_tag in soup.find_all("section", attrs={"data-type": "section"}):
        plan["sections"].append(_parse_section(sec_tag))

    html_stem = os.path.splitext(os.path.basename(html_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "plan.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    return out_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python html_to_content_plan.py <input_html> <output_dir>")
    else:
        out = parse_html_to_content_plan(sys.argv[1], sys.argv[2])
        print(f"✅ Success: {out}")
