import os

from markdown_blocks import markdown_to_blocks
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("no header (h1) found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as markdown_file:
        md_content = markdown_file.read()
    with open(template_path) as template_file:
        template_content = template_file.read()

    html_string = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)

    site_with_title = template_content.replace("{{ Title }}", title, 1)
    full_site = site_with_title.replace("{{ Content }}", html_string)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, "w") as file:
        file.write(full_site)