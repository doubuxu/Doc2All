"""
pipeline.py
-----------
海报数据生成流水线。

对外接口：
    single_data_generate(image_path, mineru_path, output_path)
        处理单张海报图片，生成 HTML、复制子图、解析并补全 JSON。

    batch_generate(image_dir, mineru_path, output_path)
        批量处理 image_dir 下所有图片（jpg/jpeg/png），串行调用 single_data_generate。
"""

import os
import random
import time
import shutil
from pathlib import Path
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# 或者获取当前工作目录
# current_dir = os.getcwd()

# 插入到路径列表的最前面（优先搜索）
sys.path.insert(0, current_dir)
from planJson3 import parse_html_to_content_plan
from ImageInfo import enrich_content_plan2
from htmlGenerate4 import responsiveHTMLGenerate   # 调用方自行提供


# 支持的图片扩展名
_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}

# mineru 输出中存放子图的三个子目录
_VISUAL_SUBDIRS = ["visuals/equations", "visuals/images", "visuals/tables"]


def single_data_generate(image_path: str, mineru_path: str, output_path: str) -> None:
    """
    处理单张海报图片，完整流程：
      1. 调用 responsiveHTMLGenerate 生成 HTML 字符串
      2. 在 output_path/<image_name>/ 下保存 poster.html
      3. 将三个子图目录（equations / images / tables）下的所有图片
         平铺复制到 output_path/<image_name>/（与 HTML 同层，不建子文件夹）
      4. 解析 poster.html → output_path/<image_name>/plan.json
      5. 调用大模型补全 plan.json 中的尺寸与语义描述，原地写回

    参数
    ----
    image_path  : 海报图片的完整路径
    mineru_path : MinerU 输出根目录（内含以 image_name 命名的子文件夹）
    output_path : 输出根目录
    """
    image_name = Path(image_path).stem

    # ── 1. 生成 HTML ──────────────────────────────────────────────────────────
    print(f"[{image_name}] 生成 HTML ...")
    html_data = responsiveHTMLGenerate(image_path, mineru_path)

    # ── 2. 创建输出目录，保存 HTML ────────────────────────────────────────────
    item_dir = Path(output_path) / image_name
    item_dir.mkdir(parents=True, exist_ok=True)

    html_path = item_dir / "poster.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_data)
    print(f"[{image_name}] HTML 已保存: {html_path}")

    # ── 3. 复制子图（equations / images / tables）→ item_dir 平铺 ────────────
    mineru_item_dir = Path(mineru_path) / image_name
    copied = 0
    for subdir in _VISUAL_SUBDIRS:
        src_dir = mineru_item_dir / subdir
        if not src_dir.is_dir():
            print(f"[{image_name}] [SKIP] 子图目录不存在: {src_dir}")
            continue
        for img_file in src_dir.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in _IMAGE_SUFFIXES:
                dest = item_dir / img_file.name
                shutil.copy2(img_file, dest)
                copied += 1
    print(f"[{image_name}] 子图复制完成，共 {copied} 张")

    # ── 4. 解析 HTML → plan.json ──────────────────────────────────────────────
    json_path = str(item_dir / "plan.json")
    print(f"[{image_name}] 解析 HTML → JSON ...")
    parse_html_to_content_plan(html_path=str(html_path), output_dir=str(item_dir))
    # parse_html_to_content_plan 输出文件名与 HTML 同名（poster.json），重命名为 plan.json
    default_json = item_dir / "poster.json"
    if default_json.exists() and not Path(json_path).exists():
        default_json.rename(json_path)

    # ── 5. 补全 JSON（尺寸 + 语义）────────────────────────────────────────────
    print(f"[{image_name}] 补全 JSON 信息 ...")
    enrich_content_plan2(json_path=json_path)

    print(f"[{image_name}] ✅ 完成\n")


def batch_generate(image_dir: str, mineru_path: str, output_path: str) -> None:
    """
    批量处理 image_dir 下所有图片，串行调用 single_data_generate。

    参数
    ----
    image_dir   : 海报图片所在文件夹
    mineru_path : MinerU 输出根目录
    output_path : 输出根目录
    """
    image_dir_p = Path(image_dir)
    images = sorted(
        p for p in image_dir_p.iterdir()
        if p.is_file() and p.suffix.lower() in _IMAGE_SUFFIXES
    )

    if not images:
        print(f"[batch] 未在 {image_dir} 下找到图片文件")
        return

    print(f"[batch] 共找到 {len(images)} 张图片，开始处理...\n")
    for idx, img_path in enumerate(images, 1):
        print(f"{'='*60}")
        print(f"[batch] ({idx}/{len(images)}) {img_path.name}")
        print(f"{'='*60}")
        try:
            single_data_generate(
                image_path=str(img_path),
                mineru_path=mineru_path,
                output_path=output_path,
            )
        except Exception as e:
            print(f"[batch] [ERROR] {img_path.name} 处理失败: {e}\n")
            
        wait = random.uniform(5, 10)
        print(f"[batch] 等待 {wait:.1f} 秒...\n")
        time.sleep(wait)

    print(f"[batch] 全部处理完毕，输出目录: {output_path}")

if __name__=="__main__":
    image_path="../posterData/batch3/"
    mineru_path="../posterData/batch3/mineru_output_with_eq"
    output_path="../finetuneData/poster/batchData3"
    #image_path="../posterData/batch2/A continuous benchmarking community challenge for COVID-19 outcome prediction.jpg"
    #mineru_path="../posterData/batch2/mineru_output_with_eq"
    #output_path="./"
    #single_data_generate(image_path,mineru_path,output_path)
    batch_generate(image_path,mineru_path,output_path)