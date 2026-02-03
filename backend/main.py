import os
from http import HTTPStatus

from fastapi import FastAPI

from endpoints import endpoint_router
from services.convert_service import convert_png_to_jpg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.include_router(endpoint_router)


@app.get("/")
async def main():
    return {"Message": "Hello World!"}
