from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from services.convert_service import convert_jpg_to_png, convert_png_to_jpg
from utils import filter_file_name

img_convert = APIRouter(prefix="/convert")


@img_convert.post("/PNGtoJPG")
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


@img_convert.post("/JPGtoPNG")
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
