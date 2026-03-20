import copy
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import load_json,save_json
import json
from PIL import Image

import copy

def restore_middle_json_coords(middle_json, img_w, img_h):
    """
    将 middle_json 中所有 bbox 坐标从其内部坐标系（page_size）缩放到原图尺寸。
 
    middle_json 内部使用自己的 page_size（如 2488×1658）作为坐标空间，
    本函数将所有层级的 bbox 等比缩放到 img_w × img_h。
 
    参数:
        middle_json : dict  -- 原始 middle_json 内容（不会修改原对象）
        img_w       : int   -- 原图宽度（像素）
        img_h       : int   -- 原图高度（像素）
 
    返回:
        dict -- 坐标已复原的新 middle_json（深拷贝，原对象不变）
    """
    result = copy.deepcopy(middle_json)
 
    for page in result.get("pdf_info", []):
        page_size = page.get("page_size", None)
        if page_size is None:
            continue
 
        mid_w, mid_h = page_size[0], page_size[1]
        sx = img_w / mid_w   # x 方向缩放比
        sy = img_h / mid_h   # y 方向缩放比
 
        def scale_bbox(bbox):
            """将单个 [x0, y0, x1, y1] 按缩放比转换"""
            return [
                bbox[0] * sx,
                bbox[1] * sy,
                bbox[2] * sx,
                bbox[3] * sy,
            ]
 
        def rescale_block(block):
            """递归缩放一个块内所有层级的 bbox"""
            if "bbox" in block:
                block["bbox"] = scale_bbox(block["bbox"])
 
            # image/table 顶层块的子块列表
            for sub in block.get("blocks", []):
                rescale_block(sub)
 
            # 文本行
            for line in block.get("lines", []):
                if "bbox" in line:
                    line["bbox"] = scale_bbox(line["bbox"])
                # span 级别
                for span in line.get("spans", []):
                    if "bbox" in span:
                        span["bbox"] = scale_bbox(span["bbox"])
 
        # 处理 para_blocks 和 discarded_blocks
        for block in page.get("para_blocks", []):
            rescale_block(block)
        for block in page.get("discarded_blocks", []):
            rescale_block(block)
 
        # page_size 同步更新
        page["page_size"] = [img_w, img_h]
 
    return result

def restore_bbox_to_pixel(content_list, img_w, img_h):
    import copy
    new_list = copy.deepcopy(content_list)
    
    def process_item(item):
        if "bbox" in item:
            x0, y0, x1, y1 = item["bbox"]
            # 还原公式： 坐标 * 实际尺寸 / 1000
            item["bbox"] = [
                int(x0 * img_w / 1000),
                int(y0 * img_h / 1000),
                int(x1 * img_w / 1000),
                int(y1 * img_h / 1000)
            ]
        # 递归处理子层级 (lines, spans 等)
        for key in ["lines", "spans", "para_blocks", "list_items"]:
            if key in item and isinstance(item[key], list):
                for sub_item in item[key]:
                    if isinstance(sub_item, dict):
                        process_item(sub_item)
    
    for entry in new_list:
        process_item(entry)
    return new_list

def get_image_size(path):
    w, h = Image.open(path).size
    return w,h




import json
import os

def generate_poster_html(content_list, middle_json, img_w, img_h, output_path="poster_layout.html"):
    CAPTION_FONT_SIZE = 9
    content_list = restore_bbox_to_pixel(content_list, img_w, img_h)
    middle_json  = restore_middle_json_coords(middle_json, img_w, img_h)

    page_info = middle_json.get("pdf_info", [{}])[0]
    all_mid_blocks = (
        page_info.get("para_blocks", []) +
        page_info.get("discarded_blocks", [])
    )

    def overlap_area(a, b):
        ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
        iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
        return ix * iy

    def find_best_block(bbox, block_types=None):
        best, best_area = None, 0.0
        for blk in all_mid_blocks:
            if block_types and blk.get("type") not in block_types:
                continue
            area = overlap_area(bbox, blk.get("bbox", [0, 0, 0, 0]))
            if area > best_area:
                best_area = area
                best = blk
        return best if best_area > 0 else None

    def estimate_font_size(bbox, text="", fallback_lines=1):
        bbox_h = max(1, bbox[3] - bbox[1])
        mid_blk = find_best_block(bbox)
        line_count = None

        if mid_blk is not None:
            if "lines" in mid_blk:
                line_count = len(mid_blk["lines"])
            elif "blocks" in mid_blk:
                total = sum(len(sub.get("lines", [])) for sub in mid_blk["blocks"])
                line_count = total if total > 0 else None

        if not line_count:
            line_count = max(text.count("\n") + 1, fallback_lines)

        return max(7, round(bbox_h / max(line_count, 1) * 0.78))

    def get_visual_sub_bboxes(item):
        parent = find_best_block(item["bbox"], block_types=("image", "table"))
        body_bbox, caption_bboxes = None, []

        if parent and "blocks" in parent:
            for sub in parent["blocks"]:
                sub_bbox = sub.get("bbox")
                if sub_bbox is None:
                    continue
                sub_type = sub.get("type", "")
                if "body" in sub_type:
                    body_bbox = sub_bbox
                elif "caption" in sub_type:
                    caption_bboxes.append(sub_bbox)

        return body_bbox, caption_bboxes

    html_parts = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #c8c8c8;
    display: flex;
    justify-content: center;
    padding: 20px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }}
  #poster {{
    position: relative;
    width: {img_w}px;
    height: {img_h}px;
    background: #fff;
    box-shadow: 0 4px 28px rgba(0,0,0,0.3);
    overflow: hidden;
  }}
  .blk {{
    position: absolute;
    overflow: hidden;
    word-wrap: break-word;
    line-height: 1.25;
  }}
  .t-header  {{ font-weight: bold; }}
  .t-title   {{ font-weight: bold; }}
  .t-footer  {{ color: #888; }}
  .t-text    {{ color: #111; }}
  .t-caption {{
    font-style: italic;
    color: #444;
    text-align: center;
    font-size: {CAPTION_FONT_SIZE}px;
    line-height: 1.3;
  }}
  .t-list {{ color: #111; }}
  .t-equation {{ text-align: center; }}  /* ← NEW */
  ul {{ list-style-type: disc; padding-left: 1.3em; margin: 0; }}
  li {{ margin-bottom: 2px; }}
  img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
</style>
</head>
<body>
<div id="poster">
"""]

    def emit(bbox, css_class, inner_html, extra_style=""):
        x0, y0, x1, y1 = bbox
        w = max(1, x1 - x0)
        h = max(1, y1 - y0)
        style = f"left:{x0:.1f}px;top:{y0:.1f}px;width:{w:.1f}px;height:{h:.1f}px;{extra_style}"
        html_parts.append(f'<div class="blk {css_class}" style="{style}">{inner_html}</div>\n')

    def emit_visual(item, img_src):
        body_bbox, cap_bboxes = get_visual_sub_bboxes(item)
        render_bbox = body_bbox if body_bbox else item["bbox"]

        emit(render_bbox, "t-visual", f'<img src="{img_src}" alt="">')

        cap_key = "image_caption" if item.get("type") == "image" else "table_caption"
        cap_texts = item.get(cap_key, [])

        if cap_bboxes:
            for cb, ct in zip(cap_bboxes, cap_texts or [""]):
                emit(cb, "t-caption", ct)
            for ct in cap_texts[len(cap_bboxes):]:
                x0, _, x1, y1 = render_bbox
                emit([x0, y1, x1, y1 + 16], "t-caption", ct)
        elif cap_texts:
            x0, _, x1, y1 = render_bbox
            emit([x0, y1, x1, y1 + 16], "t-caption", " ".join(cap_texts))

    # ── 遍历 content_list ──────────────────────────────────────────────────────
    for item in content_list:
        itype = item.get("type", "text")
        bbox  = item.get("bbox", [0, 0, 0, 0])

        if itype == "image":
            raw_path = item.get("img_path", "")
            src = f"./{os.path.basename(raw_path)}" if raw_path else "./placeholder.jpg"
            emit_visual(item, src)

        elif itype == "table":
            raw_path = item.get("img_path", "")
            src = f"./{os.path.basename(raw_path)}" if raw_path else "./placeholder.jpg"
            emit_visual(item, src)

        # ← NEW: 公式用图片渲染，居中显示
        elif itype == "equation":
            raw_path = item.get("img_path", "")
            src = f"./{os.path.basename(raw_path)}" if raw_path else "./placeholder.jpg"
            emit(bbox, "t-equation", f'<img src="{src}" alt="{item.get("text", "")}">')

        elif itype == "list":
            items    = item.get("list_items", [])
            all_text = " ".join(items)
            fs = estimate_font_size(bbox, all_text, fallback_lines=len(items))
            li_html = "".join(f"<li>{t}</li>" for t in items)
            emit(bbox, "t-list", f"<ul>{li_html}</ul>",
                 f"font-size:{fs}px;line-height:1.3;")

        elif itype == "header":
            text = item.get("text", "")
            fs   = estimate_font_size(bbox, text)
            emit(bbox, "t-header", text, f"font-size:{fs}px;line-height:1.2;")

        elif itype == "footer":
            text = item.get("text", "")
            fs   = estimate_font_size(bbox, text)
            emit(bbox, "t-footer", text, f"font-size:{fs}px;")

        else:  # text（含 text_level）
            text       = item.get("text", "")
            text_level = item.get("text_level", 0)
            fs         = estimate_font_size(bbox, text)
            css = "t-title" if text_level == 1 else "t-text"
            lh  = "1.2" if text_level == 1 else "1.3"
            emit(bbox, css, text, f"font-size:{fs}px;line-height:{lh};")

    html_parts.append("</div>\n</body>\n</html>")

    full_html = "".join(html_parts)
    return full_html

# 使用示例
# generate_precise_html(content_list_data, middle_json_data, 2488, 1658)
if __name__=="__main__":
    content_list_path="../posterData/mineru_output/A View From Somewhere: Human-Centric Face Representations_poster/A View From Somewhere: Human-Centric Face Representations_poster_content_list.json"
    content_list=load_json(content_list_path)
    image_path="../posterData/A View From Somewhere: Human-Centric Face Representations_poster.jpg"
    w,h=get_image_size(image_path)
    content_list=restore_bbox_to_pixel(content_list,w,h)
    middle_json_path="../posterData/mineru_output/A View From Somewhere: Human-Centric Face Representations_poster/A View From Somewhere: Human-Centric Face Representations_poster_middle.json"
    middle_json=load_json(middle_json_path)
    middle_json=restore_middle_json_coords(middle_json,w,h)
    generate_poster_html(content_list,middle_json,w,h,"poster2.html")
