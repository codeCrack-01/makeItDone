import io

import numpy as np
from PIL import Image

from services.img_services import compress_service, convert_service

# ========================================================================= #
# ------------------------------Unit Tests--------------------------------- #
# ========================================================================= #


def test_convert_service__png_to_jpg():
    input_buffer = io.BytesIO()
    Image.new("RGBA", (10, 10), color="blue").save(input_buffer, format="PNG")
    png_bytes = input_buffer.getvalue()

    result_buffer = convert_service.convert_png_to_jpg(png_bytes)
    assert isinstance(result_buffer, io.BytesIO)

    output_image = Image.open(result_buffer)
    assert output_image.format == "JPEG"
    assert output_image.mode == "RGB"


def test_convert_service__jpg_to_png():
    input_buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="green").save(input_buffer, format="JPEG")
    jpg_bytes = input_buffer.getvalue()

    result_buffer = convert_service.convert_jpg_to_png(jpg_bytes)
    assert isinstance(result_buffer, io.BytesIO)

    output_image = Image.open(result_buffer)
    assert output_image.format == "PNG"
    assert output_image.mode == "RGBA"


def test_compress_service__image_size_to_200kb():
    img = Image.new("RGB", (2000, 2000), color="white")
    pixels = img.load()

    assert pixels is not None

    for x in range(0, 2000, 10):
        for y in range(0, 2000, 10):
            pixels[x, y] = (x % 255, y % 255, (x + y) % 255)

    result_buffer = compress_service.compress_jpg_to_200kb(img)

    size_kb = len(result_buffer.getvalue()) / 1024
    assert size_kb <= 200
    assert result_buffer.getvalue().startswith(
        b"\xff\xd8"
    )  # Valid JPEG header (just copied from internet)


def test_compress_service__image_forces_resize_on_huge_images():  # THIS IS AN EDGE_CASE !
    huge_img = Image.fromarray(
        np.random.randint(0, 255, (5000, 5000, 3), dtype=np.uint8)
    )

    result_buffer = compress_service.compress_jpg_to_200kb(huge_img)

    size_kb = len(result_buffer.getvalue()) / 1024
    assert size_kb <= 200

    final_img = Image.open(result_buffer)
    assert final_img.width < 5000  # Now this should actually be triggered!


# ========================================================================= #
# --------------------------Integration Tests------------------------------ #
# ========================================================================= #


async def test_convert__png_to_jpg(client):
    file_content = io.BytesIO()
    Image.new("RGBA", (10, 10), color="red").save(file_content, format="PNG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/png")}
    response = await client.post("/api/images/png_to_jpg", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


async def test_convert__jpg_to_png(client):
    file_content = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(file_content, format="JPEG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/jpg")}
    response = await client.post("/api/images/jpg_to_png", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


async def test_compress__compress_img_to_200kb(client):
    # Large 2000x2000 PNG
    img = Image.new("RGBA", (2000, 2000), color=(255, 0, 0, 255))
    img_buf = io.BytesIO()
    img.save(img_buf, format="PNG")

    files = {"file": ("test.png", img_buf.getvalue(), "image/png")}
    response = await client.post("/api/images/compress_to_200kb", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert len(response.content) <= 200 * 1024
