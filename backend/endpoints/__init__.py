from fastapi import APIRouter

from .img_conv import img_api
from .pdf_conv import pdf_api

endpoint_router = APIRouter(prefix="/api", tags=["api"])

endpoint_router.include_router(img_api)
endpoint_router.include_router(pdf_api)
