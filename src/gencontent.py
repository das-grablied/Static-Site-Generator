import os

from markdown_blocks import markdown_to_html_node
from pathlib import Path


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}...")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        raw_template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)
    with_title = raw_template.replace("{{ Title }}", title)
    final_html = with_title.replace("{{ Content }}", html)
    href = final_html.replace('href="/', 'href="' + basepath)
    src = href.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)

    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(src)


def generate_pages_recursive(from_dir, template_path, dest_dir, basepath):
    for entry in os.listdir(from_dir):
        from_path = os.path.join(from_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(
                from_path, template_path, dest_path, basepath)
