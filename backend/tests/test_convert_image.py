import io

from PIL import Image

from services import convert_service

# ======================================================================== #
# ------------------------------Unit Test--------------------------------- #
# ======================================================================== #


async def test_convert_service__png_to_jpg():
    input_buffer = io.BytesIO()
    Image.new("RGBA", (10, 10), color="blue").save(input_buffer, format="PNG")
    png_bytes = input_buffer.getvalue()

    result_buffer = convert_service.convert_png_to_jpg(png_bytes)
    assert isinstance(result_buffer, io.BytesIO)

    output_image = Image.open(result_buffer)
    assert output_image.format == "JPEG"
    assert output_image.mode == "RGB"


async def test_convert_service__jpg_to_png():
    input_buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="green").save(input_buffer, format="JPEG")
    jpg_bytes = input_buffer.getvalue()

    result_buffer = convert_service.convert_jpg_to_png(jpg_bytes)
    assert isinstance(result_buffer, io.BytesIO)

    output_image = Image.open(result_buffer)
    assert output_image.format == "PNG"
    assert output_image.mode == "RGBA"


# ======================================================================== #
# --------------------------Integration Test------------------------------ #
# ======================================================================== #


async def test_convert__png_to_jpg(client):
    file_content = io.BytesIO()
    Image.new("RGBA", (10, 10), color="red").save(file_content, format="PNG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/png")}
    response = await client.post("/convert/PNGtoJPG", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


async def test_convert__jpg_to_png(client):
    file_content = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(file_content, format="JPEG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/jpg")}
    response = await client.post("/convert/JPGtoPNG", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
