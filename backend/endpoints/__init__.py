from fastapi import APIRouter

from .converter import convert_api

endpoint_router = APIRouter()

endpoint_router.include_router(convert_api)
