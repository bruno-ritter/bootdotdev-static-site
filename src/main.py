import os
import shutil
import sys
from pathlib import Path

from markdown_to_html import extract_title, markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        md: str = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template: str = f.read()

    html_node = markdown_to_html_node(md)
    html_str = html_node.to_html()
    title_page: str | None = extract_title(md)
    content: str = (
        template.replace("{{ Title }}", title_page)
        .replace("{{ Content }}", html_str)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def copy_files(source_path: str, destination_path: str) -> None:
    source_path = os.path.abspath(source_path)
    destination_path = os.path.abspath(destination_path)

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        dest_path = os.path.join(destination_path, filename)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files(from_path, dest_path)


def main() -> None:

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
