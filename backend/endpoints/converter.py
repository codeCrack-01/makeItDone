import io
from datetime import datetime
from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from services.convert_service import (
    convert_images_to_pdf,
    convert_jpg_to_png,
    convert_png_to_jpg,
)
from utils import filter_file_name

convert_api = APIRouter(prefix="/convert")


@convert_api.post("/png_to_jpg")
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


@convert_api.post("/jpg_to_png")
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


@convert_api.post("/images_to_pdf")
async def convert__images_to_pdf(files: List[UploadFile] = File(...)):
    image_buffers = [io.BytesIO(await file.read()) for file in files]

    time_stamp = datetime.now().isoformat()

    pdf_result = convert_images_to_pdf(image_buffers)
    if pdf_result is None:
        return {"error": "Invalid Image OR Image Not Found !"}

    return StreamingResponse(
        pdf_result,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={time_stamp}.pdf"},
    )
