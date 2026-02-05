import io
from datetime import datetime
from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from services.pdf_service import convert_images_to_pdf, convert_pdf_to_images

pdf_api = APIRouter(prefix="/pdf", tags=["pdf"])


@pdf_api.post("/images_to_pdf", tags=["convert"])
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


@pdf_api.post("/pdf_to_images", tags=["convert"])
async def convert__pdf_to_images(file: UploadFile = File(...)):
    pdf_buffer = io.BytesIO(await file.read())

    zip_result = convert_pdf_to_images(pdf_buffer)

    return StreamingResponse(
        zip_result,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=converted_pages.zip"},
    )
