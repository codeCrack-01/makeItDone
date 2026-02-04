from pathlib import Path

from PIL import Image


def image_generator(image_list):
    for img_path in image_list:
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        yield img


def filter_file_name(name_str):
    if name_str is not None:
        return Path(name_str).stem
