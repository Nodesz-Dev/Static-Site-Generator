import os
import shutil
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

PUBLIC_DIRECTORY = "/home/brain/workspace/github.com/Static-Site-Generator/public"
STATIC_DIRECTORY = "/home/brain/workspace/github.com/Static-Site-Generator/static"
CONTENT_DIRECTORY = "/home/brain/workspace/github.com/Static-Site-Generator/content"
TEMPLATE_PATH = "/home/brain/workspace/github.com/Static-Site-Generator/template.html"


def main():

    CopySourceFiles(STATIC_DIRECTORY, PUBLIC_DIRECTORY, True)

    if check_paths():
        generate_page(os.path.join(CONTENT_DIRECTORY, "index.md"),
                        TEMPLATE_PATH,
                        os.path.join(PUBLIC_DIRECTORY, "index.html"))
    else:
        raise Exception("Something went wrong, a path is missing")

def CopySourceFiles(src, dst, cleardir=False):
    if not os.path.exists(src):
        raise ValueError(f"Error: {src} file location does not exist")
    
    if cleardir:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        pass

    file_list = os.listdir(src)
    for file in file_list:
        full_path = os.path.join(src,file)
        if os.path.isfile(full_path):
            shutil.copy(full_path, dst)
        elif os.path.isdir(full_path):
            dirpath = os.path.join(dst, file)
            os.mkdir(dirpath)
            CopySourceFiles(os.path.join(src, file), dirpath)
        else:
            raise Exception(f"Error: Something went wrong with file at path {file}")

def generate_page(from_path, template_path, dest_path):
    print (f" Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, "r")
    markdown_contents = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(markdown_contents)
    html_content = html_node.to_html()
    title = extract_title(markdown_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_content)

    dest_dirs = os.path.dirname(dest_path)
    if dest_dirs != "":
        os.makedirs(dest_dirs, exist_ok=True)

    dest_file = open(dest_path, "w")
    dest_file.write(template_contents)

def check_paths():
    all_clear = True
    if not os.path.exists(CONTENT_DIRECTORY):
        print ("Content Path does not exist")
        all_clear = False
    if not os.path.exists(os.path.join(CONTENT_DIRECTORY, "index.md")):
        print ("index.md does not exist")
        all_clear = False
    if not os.path.exists(PUBLIC_DIRECTORY):
        print ("Public Path does not exist")
        all_clear = False
    if not os.path.exists(TEMPLATE_PATH):
        print ("Template does not exist")
        all_clear = False
    if not os.path.exists(STATIC_DIRECTORY):
        print ("Static path does not exist")
        all_clear = False

    return all_clear

main()