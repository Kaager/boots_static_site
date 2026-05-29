import os
import shutil

from generate_page import generate_page, generate_page_recursive

def main():
    static_path = "./static"
    public_path = "./public"
    prepare_static_to_public(static_path, public_path)

    generate_page_recursive("./content", "./template.html", "./public")


def prepare_static_to_public(static_path, public_path):
    if not os.path.exists(static_path):
        raise Exception("Path does not exist (static)")
    
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    copy_static_to_public(static_path, public_path)


def copy_static_to_public(static_path, public_path):
    items = os.listdir(static_path)

    for item in items:
        file_path = os.path.join(static_path, item)
        public_file_path = os.path.join(public_path, item)
        if os.path.isfile(file_path):
            print(f"Copying {file_path} -> {public_file_path}")
            shutil.copy(file_path, public_file_path)
        elif os.path.isdir(file_path):
            os.mkdir(public_file_path)
            copy_static_to_public(file_path, public_file_path)

main()