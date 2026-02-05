import io
import zipfile
from typing import Iterable

from pdf2image import convert_from_bytes

from utils import image_generator

from .img_services.modify_service import compress_jpg_to_200kb


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


def convert_pdf_to_images(pdf_buffer: io.BytesIO) -> io.BytesIO:
    pdf_buffer.seek(0)
    images = convert_from_bytes(pdf_buffer.read())

    zip_output = io.BytesIO()
    with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(images):
            compressed_buf = compress_jpg_to_200kb(img)
            zf.writestr(f"page_{i + 1}.jpg", compressed_buf.getvalue())

    zip_output.seek(0)
    return zip_output
