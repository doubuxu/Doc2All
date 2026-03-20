import copy
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import load_json,save_json
import json
import cv2
import numpy as np
from typing import List, Dict, Tuple, Union
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
def rescale_content_list(content_list, middle_json, img_w, img_h):
    """
    根据 middle.json 中的 page_size 将 content_list 的坐标缩放到图片像素尺寸
    
    Args:
        content_list: 待修改的 content_list 列表
        middle_json: MinerU 输出的完整 JSON 字典（包含 pdf_info 和 page_size）
        img_w: 原始海报图片的像素宽度
        img_h: 原始海报图片的像素高度
        
    Returns:
        修改完 bbox 的 content_list
    """
    # 1. 从 middle_json 中安全获取 page_size
    # 假设处理的是第一页 (page_idx: 0)
    try:
        pdf_w, pdf_h = middle_json["pdf_info"][0]["page_size"]
        print(f"pdf_w:{pdf_w}")
        print(f"pdf_h:{pdf_h}")
    except (KeyError, IndexError):
        print("Error: 无法从 middle_json 中找到 page_size")
        return content_list

    # 2. 计算缩放比例
    scale_x = img_w / pdf_w
    scale_y = img_h / pdf_h

    def rescale_bbox(bbox):
        """内部辅助函数：执行具体的缩放计算"""
        if not bbox or len(bbox) != 4:
            return bbox
        return [
            int(bbox[0] * scale_x),
            int(bbox[1] * scale_y),
            int(bbox[2] * scale_x),
            int(bbox[3] * scale_y)
        ]

    def process_recursive(item):
        """递归遍历并修改所有包含 bbox 的字典"""
        if isinstance(item, dict):
            # 如果当前字典有 bbox 字段，直接修改
            if "bbox" in item:
                item["bbox"] = rescale_bbox(item["bbox"])
            
            # 递归处理字典中的所有 key (如 lines, spans, blocks 等)
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    process_recursive(value)
        elif isinstance(item, list):
            # 如果是列表，遍历列表中的每一项
            for element in item:
                process_recursive(element)

    # 3. 深拷贝原始数据并执行递归修改
    new_content_list = copy.deepcopy(content_list)
    process_recursive(new_content_list)

    return new_content_list

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

def draw_bbox_on_image(
    image_path: Union[str, Path],
    detection_json: Union[str, Path, List[Dict]],
    output_path: Union[str, Path] = None,
    show: bool = True,
    colors: Dict[str, Tuple[int, int, int]] = None
) -> np.ndarray:
    """
    在原图上绘制 image 和 table 类型的 bbox
    
    Args:
        image_path: 原图路径
        detection_json: 检测结果JSON路径或JSON列表
        output_path: 输出图片路径（可选）
        show: 是否显示结果
        colors: 自定义颜色字典，格式为 {'image': (B,G,R), 'table': (B,G,R)}
    
    Returns:
        绘制了bbox的图像数组
    """
    
    # 默认颜色配置 (BGR格式，OpenCV使用)
    if colors is None:
        colors = {
            'image': (0, 165, 255),    # 橙色
            'table': (0, 255, 0)       # 绿色
        }
    
    # 读取原图
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"无法读取图片: {image_path}")
    
    # 创建副本用于绘制
    result_image = image.copy()
    
    # 解析JSON
    if isinstance(detection_json, (str, Path)):
        with open(detection_json, 'r', encoding='utf-8') as f:
            detections = json.load(f)
    else:
        detections = detection_json
    
    # 统计绘制的bbox数量
    draw_count = {'image': 0, 'table': 0}
    
    # 遍历检测结果，只处理 image 和 table 类型
    for item in detections:
        item_type = item.get('type', '').lower()
        
        if item_type not in ['image', 'table']:
            continue
        
        # 获取bbox坐标 [x1, y1, x2, y2]
        bbox = item.get('bbox')
        if bbox is None or len(bbox) != 4:
            print(f"警告: 跳过无效的bbox: {bbox}")
            continue
        
        x1, y1, x2, y2 = map(int, bbox)
        
        # 确保坐标在图像范围内
        h, w = result_image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        # 绘制矩形框
        color = colors.get(item_type, (128, 128, 128))
        thickness = 3
        cv2.rectangle(result_image, (x1, y1), (x2, y2), color, thickness)
        
        # 绘制标签背景
        label = f"{item_type.upper()}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        
        (text_w, text_h), _ = cv2.getTextSize(label, font, font_scale, font_thickness)
        
        # 标签背景矩形
        label_bg_x1 = x1
        label_bg_y1 = y1 - text_h - 10
        label_bg_x2 = x1 + text_w + 10
        label_bg_y2 = y1
        
        # 如果标签会超出图像顶部，则放在bbox下方
        if label_bg_y1 < 0:
            label_bg_y1 = y2
            label_bg_y2 = y2 + text_h + 10
        
        cv2.rectangle(
            result_image,
            (label_bg_x1, label_bg_y1),
            (label_bg_x2, label_bg_y2),
            color,
            -1  # 填充
        )
        
        # 绘制标签文字
        cv2.putText(
            result_image,
            label,
            (label_bg_x1 + 5, label_bg_y2 - 5),
            font,
            font_scale,
            (255, 255, 255),  # 白色文字
            font_thickness
        )
        
        draw_count[item_type] += 1
    
    print(f"绘制完成: {draw_count['image']} 个 image, {draw_count['table']} 个 table")
    
    # 保存结果
    if output_path:
        cv2.imwrite(str(output_path), result_image)
        print(f"结果已保存至: {output_path}")
    
    # 显示结果
    if show:
        # 转换BGR为RGB用于matplotlib显示
        result_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
        
        plt.figure(figsize=(16, 12))
        plt.imshow(result_rgb)
        plt.axis('off')
        plt.title(f"Detection Result: {draw_count['image']} images, {draw_count['table']} tables")
        plt.tight_layout()
        plt.show()
    
    return result_image


def batch_process(
    image_dir: Union[str, Path],
    json_dir: Union[str, Path],
    output_dir: Union[str, Path],
    image_extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
) -> None:
    """
    批量处理文件夹中的图片和对应的JSON文件
    
    假设JSON文件名与图片文件名对应（仅扩展名不同）
    """
    image_dir = Path(image_dir)
    json_dir = Path(json_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有图片
    image_files = []
    for ext in image_extensions:
        image_files.extend(image_dir.glob(f'*{ext}'))
    
    print(f"找到 {len(image_files)} 张图片")
    
    for img_path in image_files:
        # 查找对应的JSON文件
        json_path = json_dir / f"{img_path.stem}.json"
        
        if not json_path.exists():
            # 尝试其他可能的命名方式
            json_path = json_dir / f"{img_path.stem}_result.json"
        
        if json_path.exists():
            output_path = output_dir / f"{img_path.stem}_visualized{img_path.suffix}"
            try:
                draw_bbox_on_image(
                    img_path,
                    json_path,
                    output_path=output_path,
                    show=False
                )
            except Exception as e:
                print(f"处理 {img_path.name} 时出错: {e}")
        else:
            print(f"未找到 {img_path.name} 对应的JSON文件")

def get_image_size(path):
    w, h = Image.open(path).size
    return w,h

# ==================== 使用示例 ====================

if __name__ == "__main__":
    
    # 示例1: 单张图片处理
    # 假设你的JSON文件路径为 detection_result.json，图片路径为 input_image.jpg
    
    # 首先，创建一个示例JSON（基于你提供的格式）
    """
    sample_json = [
        {
            "type": "image",
            "img_path": "../posterData/mineru_output/[Re] Graph Edit Networks_poster/visuals/images/fig_1.jpg",
            "bbox": [28, 336, 302, 418],
            "page_idx": 0
        },
        {
            "type": "table",
            "table_body": "<table>...</table>",
            "bbox": [367, 827, 497, 935],
            "page_idx": 0
        },
        {
            "type": "text",  # 这个不会被绘制
            "text": "Some text",
            "bbox": [25, 179, 304, 334],
            "page_idx": 0
        }
    ]
    
    # 保存示例JSON
    with open("sample_detection.json", "w", encoding="utf-8") as f:
        json.dump(sample_json, f, indent=2, ensure_ascii=False)
    
    print("示例JSON已保存到 sample_detection.json")
    print("\n使用说明:")
    print("1. 单张图片处理:")
    print("   result = draw_bbox_on_image('your_image.jpg', 'detection.json', 'output.jpg')")
    print("\n2. 批量处理:")
    print("   batch_process('images/', 'jsons/', 'outputs/')")
    print("\n3. 直接使用JSON数据:")
    print("   result = draw_bbox_on_image('image.jpg', json_data_list)")
    
    # 如果你有实际的图片和JSON，取消下面的注释来运行:
    """
    # 单张处理

    layout_path = "../posterData/mineru_output/[Re] Graph Edit Networks_poster/[Re] Graph Edit Networks_poster_middle.json"
    content_list_path="../posterData/mineru_output/[Re] Graph Edit Networks_poster/[Re] Graph Edit Networks_poster_content_list.json"
    image_path="../posterData/[Re] Graph Edit Networks_poster.jpg"
    w,h=get_image_size(image_path)
    print(f"w:{w}")
    print(f"h:{h}")
    layout_json=load_json(layout_path)
    content_json=load_json(content_list_path)

    content_json=restore_bbox_to_pixel(content_json,w,h)
    save_path="./REtest.json"
    save_json(content_json,save_path)

    result = draw_bbox_on_image(
        image_path="../posterData/[Re] Graph Edit Networks_poster.jpg",
        detection_json=save_path,  # 或直接使用列表
        output_path="visualized_result.jpg",
        show=True
    )
    
    # 批量处理
    #batch_process(
    #    image_dir="./images",
    #    json_dir="./detection_results",
    #    output_dir="./visualized_outputs"
    #)
    