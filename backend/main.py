import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from endpoints import endpoint_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.include_router(endpoint_router)


@app.get("/")
async def main():
    return {"Message": "Hello World!"}


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "image-converter"}, status_code=200
    )
