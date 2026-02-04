import io
import os
from typing import Iterable

from PIL import Image

from utils import image_generator

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


def convert_images_to_pdf(image_data_list: Iterable[io.BytesIO]) -> io.BytesIO | None:
    pdf_output = io.BytesIO()
    images = image_generator(image_data_list)

    if not image_data_list:
        return None

    try:
        first_img = next(images)
    except StopIteration:
        return None

    first_img.save(pdf_output, format="PDF", save_all=True, append_images=images)

    pdf_output.seek(0)  # I hate this "seek" thing...
    return pdf_output
