import os
import shutil
from generate_page import generate_pages_recursive
import sys


def copy_directory(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Copying directory: {source_path}")
            copy_directory(source_path, dest_path)



def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    source = "static"
    destination = "docs"

    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    copy_directory(source, destination)
    
    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath,
    )

main()