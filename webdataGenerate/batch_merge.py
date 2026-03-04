import os
import sys
import fitz  # PyMuPDF


def merge_pdf_to_one_page(input_pdf_path, output_pdf_path):
    """
    将一个PDF的所有页面纵向拼接为一个单页PDF
    """

    doc = fitz.open(input_pdf_path)

    if len(doc) == 0:
        print(f"⚠️ 空文件跳过: {input_pdf_path}")
        return

    # 计算总高度和最大宽度
    total_height = 0
    max_width = 0
    page_rects = []

    for page in doc:
        rect = page.rect
        page_rects.append(rect)
        total_height += rect.height
        max_width = max(max_width, rect.width)

    # 创建新PDF
    new_doc = fitz.open()
    new_page = new_doc.new_page(width=max_width, height=total_height)

    # 逐页拼接
    current_y = 0
    for i, rect in enumerate(page_rects):
        target_rect = fitz.Rect(
            0,
            current_y,
            rect.width,
            current_y + rect.height
        )

        new_page.show_pdf_page(target_rect, doc, i)
        current_y += rect.height

    # 保存
    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()


def batch_process(input_folder, output_folder):
    """
    批量处理文件夹中的所有PDF
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"正在处理: {filename}")
            try:
                merge_pdf_to_one_page(input_path, output_path)
                print(f"✅ 已保存到: {output_path}")
            except Exception as e:
                print(f"❌ 处理失败: {filename}")
                print(e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法:")
        print("python batch_merge_pdf.py 输入PDF文件夹 输出文件夹")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    batch_process(input_folder, output_folder)