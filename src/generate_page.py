import os
from pathlib import Path

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


def generate_page_recursive(dir_path_name, template_path, dest_dir_path):

    path_content = os.listdir(dir_path_name)
    for item in path_content:
        item_path = os.path.join(dir_path_name, item)
        new_dest_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            path_with_html_suffix = Path(new_dest_item).with_suffix(".html")
            generate_page(item_path, template_path, path_with_html_suffix)

            # print(f"Generating page from {item_path} to {new_dest_item} using template at {template_path}")

            # with open(item_path) as markdown_file:
            #     md_content = markdown_file.read()
            # with open(template_path) as template_file:
            #     template_content = template_file.read()

            # html_string = markdown_to_html_node(md_content).to_html()
            # title = extract_title(md_content)

            # site_with_title = template_content.replace("{{ Title }}", title, 1)
            # full_site = site_with_title.replace("{{ Content }}", html_string)

            # if not os.path.exists(dest_dir_path):
            #     print("making that dir")
            #     os.makedirs(os.path.dirname(dest_dir_path))

            # with open(new_dest_item, "w") as file:
            #     file.write(full_site)
            

        else:
            new_dest_dir = os.path.normpath(new_dest_item)
            generate_page_recursive(item_path, template_path, new_dest_dir)