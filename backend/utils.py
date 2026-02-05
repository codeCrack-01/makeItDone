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


def get_contrast_fill_color(img: Image.Image):
    if img.mode != "RGBA":
        return (255, 255, 255)

    pixels = [p for p in list(img.getdata()) if p[3] > 0]  # type: ignore

    if not pixels:
        return (255, 255, 255)

    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)

    # ITU-R 601 Luma Transform: Humans see Green as brightest
    # L = 0.299R + 0.587G + 0.114B
    luminance = (0.299 * avg_r) + (0.587 * avg_g) + (0.114 * avg_b)

    # If the foreground is light (> 180), use a Black background.
    # If the foreground is dark (<= 180), use a White background.
    return (0, 0, 0) if luminance > 200 else (255, 255, 255)
