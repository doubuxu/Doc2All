import fitz  # PyMuPDF

# 打开原始 PDF
doc = fitz.open("../webData/web_pdf/Can LLMs Solve Molecule Puzzles_ A Multimodal Benchmark for Molecular Structure Elucidation.pdf")

page1 = doc[0]
page2 = doc[1]

# 获取页面尺寸
rect1 = page1.rect
rect2 = page2.rect

# 新建 PDF
new_doc = fitz.open()

# 创建一个新页面（高度为两页之和）
new_page = new_doc.new_page(
    width=max(rect1.width, rect2.width),
    height=rect1.height + rect2.height
)

# 将第一页插入
new_page.show_pdf_page(
    fitz.Rect(0, 0, rect1.width, rect1.height),
    doc, 0
)

# 将第二页插入（放在第一页下面）
new_page.show_pdf_page(
    fitz.Rect(0, rect1.height, rect2.width, rect1.height + rect2.height),
    doc, 1
)

# 保存
new_doc.save("merged_one_page.pdf")
new_doc.close()
doc.close()