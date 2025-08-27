import os
import shutil

PUBLIC_DIRECTORY = "/home/brain/workspace/github.com/Static-Site-Generator/public"
STATIC_DIRECTORY = "/home/brain/workspace/github.com/Static-Site-Generator/static"

def main():
    CopySourceFiles(STATIC_DIRECTORY, PUBLIC_DIRECTORY, True)
    print("done")

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

def generate_page():
    pass

main()