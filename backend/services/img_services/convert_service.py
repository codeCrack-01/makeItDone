import io
import os

from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def convert_png_to_jpg(content):
    img = Image.open(io.BytesIO(content))
    if img.format != "PNG":
        return
    rgb_img = img.convert("RGB")

    img_buffer = io.BytesIO()
    rgb_img.save(img_buffer, format="JPEG")

    # Reset the pointer to the start of the "file", its just like a "tape recorder", boring hai...
    img_buffer.seek(0)
    return img_buffer


def convert_jpg_to_png(content):
    img = Image.open(io.BytesIO(content))
    if img.format != "JPEG":
        return
    rgba_img = img.convert("RGBA")

    img_buffer = io.BytesIO()
    rgba_img.save(img_buffer, format="PNG")

    img_buffer.seek(0)
    return img_buffer
