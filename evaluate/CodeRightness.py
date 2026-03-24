import html5lib

def is_html_syntax_valid(file_path):
    """
    检查指定路径的 HTML 文件语法是否符合 HTML5 标准。
    
    Args:
        file_path (str): HTML 文件的路径。
        
    Returns:
        bool: 如果语法完全正确返回 True，否则返回 False。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用 html5lib 的严格解析模式
        # 如果代码不符合标准，它会抛出特定的 ParseError
        parser = html5lib.HTMLParser(strict=True)
        parser.parse(content)
        
        return True
    
    except html5lib.html5parser.ParseError as e:
        # 你可以在这里打印具体的错误信息，方便调试模型输出
        # print(f"解析错误: {e}")
        return False
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return False
    except Exception as e:
        # 捕获其他可能的异常（如编码问题）
        print(f"发生未知错误: {e}")
        return False

# 使用示例
# result = is_html_syntax_valid("output/poster_01.html")
# print(f"语法检查通过: {result}")

if __name__=="__main__":
    html_path="../data/output/20260322_235110_sceneGraph_poster/sceneGraph.html"
    print(is_html_syntax_valid(html_path))