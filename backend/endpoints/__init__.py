from fastapi import APIRouter

from .converter import img_convert

endpoint_router = APIRouter()

endpoint_router.include_router(img_convert)
