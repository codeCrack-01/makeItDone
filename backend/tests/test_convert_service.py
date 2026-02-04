import io

from PIL import Image

from services import convert_service

# ======================================================================== #
# ------------------------------Unit Test--------------------------------- #
# ======================================================================== #


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


def test_convert_service__images_to_pdf():
    image_buffers = []
    for color in ["red", "green", "blue"]:
        img = Image.new("RGB", (50, 50), color=color)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        image_buffers.append(img_buffer)

    result_pdf = convert_service.convert_images_to_pdf(image_buffers)

    assert isinstance(result_pdf, io.BytesIO)
    assert result_pdf.read(4) == b"%PDF"


# ======================================================================== #
# --------------------------Integration Test------------------------------ #
# ======================================================================== #


async def test_convert__png_to_jpg(client):
    file_content = io.BytesIO()
    Image.new("RGBA", (10, 10), color="red").save(file_content, format="PNG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/png")}
    response = await client.post("/convert/png_to_jpg", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


async def test_convert__jpg_to_png(client):
    file_content = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(file_content, format="JPEG")
    file_content.seek(0)

    files = {"file": ("test.png", file_content, "image/jpg")}
    response = await client.post("/convert/jpg_to_png", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


async def test_convert__images_to_pdf(client):
    img = Image.new("RGB", (10, 10), color="red")
    img_byte_arr = io.BytesIO()

    img.save(img_byte_arr, format="JPEG")
    img_data = img_byte_arr.getvalue()

    files = [
        ("files", ("image1.jpg", img_data, "image/jpeg")),
        ("files", ("image2.jpg", img_data, "image/jpeg")),
    ]

    response = await client.post("/convert/images_to_pdf", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
