import os
import json
import csv
import sys

def collect_json_data(json_root_path):
    results = []
    skipped = 0

    # 遍历目录
    for root, dirs, files in os.walk(json_root_path):
        for file in files:
            if file.lower().endswith('.json'):
                json_path = os.path.join(root, file)

                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        title = data.get("title")
                        url = data.get("url")

                        # 判断字段是否存在且非空
                        if (
                            title is not None and str(title).strip() != "" and
                            url is not None and str(url).strip() != ""
                        ):
                            results.append({
                                "title": str(title).strip(),
                                "url": str(url).strip()
                            })
                        else:
                            skipped += 1

                except Exception as e:
                    skipped += 1
                    print(f"读取失败: {json_path}, 错误: {e}")

    return results, skipped


def write_to_csv(data, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["title", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python json_to_csv.py <json文件夹路径> <输出csv路径>")
        sys.exit(1)

    json_folder = sys.argv[1]
    output_csv = sys.argv[2]

    if not os.path.isdir(json_folder):
        print(f"错误: {json_folder} 不是有效的文件夹路径")
        sys.exit(1)

    data, skipped_count = collect_json_data(json_folder)
    write_to_csv(data, output_csv)

    print(f"处理完成")
    print(f"成功写入: {len(data)} 条")
    print(f"跳过文件: {skipped_count} 个")
    print(f"输出文件: {output_csv}")