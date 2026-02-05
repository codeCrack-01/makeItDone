import io

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from services.img_services.convert_service import (
    convert_jpg_to_png,
    convert_png_to_jpg,
)
from services.img_services.modify_service import (
    compress_jpg_to_200kb,
    remove_transparency_from_image,
)
from utils import filter_file_name

img_api = APIRouter(prefix="/images", tags=["images"])


@img_api.post("/png_to_jpg", tags=["convert"])
async def convert__png_to_jpg(file: UploadFile = File(...)):
    content = await file.read()
    img_buffer = convert_png_to_jpg(content)

    original_name = filter_file_name(file.filename)

    if img_buffer is None:
        return {"error": "Image format is not PNG !"}

    return StreamingResponse(
        img_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"attachment; filename={original_name}_converted.jpg"
        },
    )


@img_api.post("/jpg_to_png", tags=["convert"])
async def convert__jpg_to_png(file: UploadFile = File(...)):
    content = await file.read()
    img_buffer = convert_jpg_to_png(content)

    original_name = filter_file_name(file.filename)

    if img_buffer is None:
        return {"error": "Image format is not JPG/JPEG !"}

    return StreamingResponse(
        img_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={original_name}_converted.png"
        },
    )


@img_api.post("/compress_to_200kb", tags=["compress"])
async def compress__image_to_200kb(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    original_name = filter_file_name(file.filename)
    compressed_buf = compress_jpg_to_200kb(img)

    return StreamingResponse(
        compressed_buf,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"attachment; filename={original_name}_compressed.jpg"
        },
    )


@img_api.post("/remove_transparency", tags=["modify"])
async def remove_transparency_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

    original_name = filter_file_name(file.filename)
    result_img = remove_transparency_from_image(img)

    buffer = io.BytesIO()
    result_img.save(buffer, format="JPEG")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"attachment; filename={original_name}_compressed.jpg"
        },
    )
