import json
import re
from pathlib import Path
from typing import Union

from PIL import Image

from changeHTMLPath import changeHTML


TABLE_IMAGE_PATTERN = re.compile(
    r"<img\b(?=[^>]*\bsrc=(['\"])(?P<src>\./(?:visuals/tables/)?(?P<table_id>table_\d+)\.(?:jpg|jpeg|png|webp))\1)[^>]*>",
    re.IGNORECASE,
)

TABLE_WRAPPER_TEMPLATE = """<div class="doc2all-table-wrapper my-8 w-full" style="aspect-ratio: {width} / {height}; min-height: 150px;">
  <div class="w-full h-full flex flex-col bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
  
    <div class="flex-grow overflow-x-auto custom-scrollbar">
    
      {table_content_slot}
    
    </div>
  
  </div>
</div>"""


def _load_table_map(doc_dir: Path) -> dict:
    tables_json_path = doc_dir / "dict" / "tables.json"
    with open(tables_json_path, "r", encoding="utf-8") as f:
        table_items = json.load(f)
    return {
        item["table_id"]: item["table_body"]
        for item in table_items
        if item.get("table_id") and item.get("table_body")
    }


def _get_image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as img:
        return img.size


def replace_table_images_with_html(html_code: str, doc_dir: Union[str, Path], log=None) -> str:
    doc_dir = Path(doc_dir)
    table_map = _load_table_map(doc_dir)
    replacement_count = 0

    def replace_match(match: re.Match) -> str:
        nonlocal replacement_count

        image_src = match.group("src")
        table_id = match.group("table_id")
        table_body = table_map.get(table_id)
        if not table_body:
            if log:
                log.warning(f"Table body not found for table_id={table_id}, keep original image tag.")
            return match.group(0)

        image_path = (doc_dir / image_src).resolve()
        if not image_path.exists():
            if log:
                log.warning(f"Table image not found: {image_path}, keep original image tag.")
            return match.group(0)

        try:
            width, height = _get_image_size(image_path)
        except Exception as exc:
            if log:
                log.warning(f"Failed to read table image size from {image_path}: {exc}. Keep original image tag.")
            return match.group(0)

        replacement_count += 1
        return TABLE_WRAPPER_TEMPLATE.format(
            width=width,
            height=height,
            table_content_slot=table_body,
        )

    updated_html = TABLE_IMAGE_PATTERN.sub(replace_match, html_code)
    if log:
        log.info(f"Replaced {replacement_count} table image reference(s) with HTML tables.")
    return updated_html


if __name__ == "__main__":
    test_doc_dir = Path("/data/huangyc/Document2All/data/output/20260322_225909_sceneGraph_web")
    input_html_path = test_doc_dir / "sceneGraph.html"
    output_html_path = test_doc_dir / "sceneGraph_table_replaced_test.html"

    html_code = input_html_path.read_text(encoding="utf-8")
    html_code = changeHTML(html_code)
    html_code = replace_table_images_with_html(html_code, test_doc_dir)
    output_html_path.write_text(html_code, encoding="utf-8")

    print(f"Saved test html to: {output_html_path}")
