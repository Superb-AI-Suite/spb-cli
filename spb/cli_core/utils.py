import re
import os
import glob
import imghdr

def get_project_config(line):
    r = re.compile(r'([^\t]*)\t*')
    return r.findall(line)

def recursive_glob_image_files(input_path):
    support_img_format = ['png', 'jpg', 'bmp', 'jpeg', 'tiff', 'tif']
    imgs_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, "**/*"), recursive=True))
    for file_path in files_path:
        if '@' not in file_path and not os.path.isdir(file_path):
            img_format = imghdr.what(file_path)
            if img_format in support_img_format:
                key = extract_file_key(input_path, file_path)
                imgs_path[key] = file_path
    return imgs_path

def recursive_glob_label_files(input_path):
    support_label_format = ['.json']
    labels_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, "**/*"), recursive=True))

    for file_path in files_path:
        if '@' not in file_path and not os.path.isdir(file_path):
            file_format = os.path.splitext(file_path)[1]
            if file_format in support_label_format:
                key = extract_file_key(input_path, file_path)
                labels_path[key] = file_path
    return labels_path

def extract_file_key(input_folder_path, file_path):
    key = os.path.abspath(file_path).replace(os.path.abspath(input_folder_path), "")
    key = "/".join(key.split("/")[1:])
    return key