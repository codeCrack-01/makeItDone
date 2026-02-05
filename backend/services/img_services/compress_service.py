import io

from PIL import Image


def compress_jpg_to_200kb(img: Image.Image) -> io.BytesIO:
    max_kb: int = 200
    target_bytes = max_kb * 1024

    for q in [85, 60, 30]:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=q, optimize=True)
        if len(buf.getvalue()) <= target_bytes:
            buf.seek(0)
            return buf

    current_img = img
    while len(buf.getvalue()) > target_bytes:
        new_size = (int(current_img.width * 0.7), int(current_img.height * 0.7))
        if new_size[0] < 100 or new_size[1] < 100:
            break

        current_img = current_img.resize(new_size, Image.LANCZOS)  # type: ignore
        buf = io.BytesIO()
        current_img.save(buf, format="JPEG", quality=20, optimize=True)

    buf.seek(0)
    return buf
