import os
import json
import chardet
import html2text
from tqdm import tqdm
from bs4 import BeautifulSoup


def extract_html(dir_path):
    files = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)

        if os.path.isdir(file_path):
            # If this is a directory, process it recursively
            files.extend(extract_html(file_path))
        elif file_name.endswith(".html"):
            files.append(file_path)
    return files


def parse_zedx(input_path, output_path, error_path):
    os.makedirs(output_path, exist_ok=True)
    files = extract_html(os.path.join(input_path, "documents"))
    error_files = []
    for file in tqdm(files, desc=input_path):
        # 跳过一些空文件
        if os.stat(file).st_size == 0:
            continue
        with open(file, "r") as f:
            try:
                html_content = f.read()
            except UnicodeDecodeError:  # 一些文件的编码不是utf-8
                rawdata = open(file, "rb").read()
                result = chardet.detect(rawdata)
                encoding = result["encoding"]
                with open(file, "r", encoding=encoding) as f:
                    html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # 找到所有class为"xref gxref"的span元素，对zedx缩略语进行补充
        for span in soup.find_all("span", class_="xref gxref"):
            title = span.get("title")
            if title:
                try:
                    en, cn = title.split("--")
                    span.string = f"{span.string}({en}, {cn})"
                except:
                    span.string = f"{span.string}({title})"
                    error_files.append(file)

        html = str(soup)
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0
        text = h.handle(html)
        path = os.path.normpath(file)
        paths = path.split(os.sep)
        try:
            paths.remove("topics")
        except ValueError:
            pass
        paths = paths[paths.index("documents") + 1 :]
        save_path = f"{os.path.splitext('/'.join(paths))[0]}.txt"
        final_save_path = os.path.join(output_path, save_path)
        os.makedirs(os.path.dirname(final_save_path), exist_ok=True)
        with open(final_save_path, "w", encoding="utf-8") as f:
            f.write(text)
    if len(error_files) > 0:
        with open(error_path, "w", encoding="utf-8") as f:
            json.dump(error_files, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_path = "director"
    output_path = "output/director"
    error_path = "output/director.json"
    parse_zedx(input_path, output_path, error_path)
