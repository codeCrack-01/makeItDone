import io
import zipfile

from PIL import Image

from services import pdf_service

# ========================================================================= #
# ------------------------------Unit Tests--------------------------------- #
# ========================================================================= #


def test_convert_service__images_to_pdf():
    image_buffers = []
    for color in ["red", "green", "blue"]:
        img = Image.new("RGB", (50, 50), color=color)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        image_buffers.append(img_buffer)

    result_pdf = pdf_service.convert_images_to_pdf(image_buffers)

    assert isinstance(result_pdf, io.BytesIO)
    assert result_pdf.read(4) == b"%PDF"


def test_convert_service__pdf_to_images():
    image_buffers = []
    for color in ["red", "green", "blue"]:
        img = Image.new("RGB", (100, 250), color=color)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
    image_buffers.append(img_buffer)

    pdf_buffer = pdf_service.convert_images_to_pdf(image_buffers)
    assert pdf_buffer is not None

    zip_buffer = pdf_service.convert_pdf_to_images(pdf_buffer)
    assert isinstance(zip_buffer, io.BytesIO)

    with zipfile.ZipFile(zip_buffer, "r") as z:
        assert len(z.namelist()) > 0
        assert z.namelist()[0].endswith(".jpg")


# ========================================================================= #
# --------------------------Integration Tests------------------------------ #
# ========================================================================= #


async def test_convert__images_to_pdf(client):
    img = Image.new("RGB", (10, 10), color="red")
    img_byte_arr = io.BytesIO()

    img.save(img_byte_arr, format="JPEG")
    img_data = img_byte_arr.getvalue()

    files = [
        ("files", ("image1.jpg", img_data, "image/jpeg")),
        ("files", ("image2.jpg", img_data, "image/jpeg")),
    ]

    response = await client.post("/api/pdf/images_to_pdf", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


async def test_convert__pdf_to_images(client):
    image_buffers = []

    for color in ["red", "green", "blue"]:
        img = Image.new("RGB", (100, 250), color=color)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

    image_buffers.append(img_buffer)
    pdf_buffer = pdf_service.convert_images_to_pdf(image_buffers)

    assert pdf_buffer is not None
    pdf_data = pdf_buffer.getvalue()

    files = {"file": ("test.pdf", pdf_data, "application/pdf")}
    response = await client.post("/api/pdf/pdf_to_images", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-zip-compressed"

    zip_bytes = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_bytes) as z:
        contents = z.namelist()
        assert len(contents) > 0
        assert contents[0].endswith(".jpg")
