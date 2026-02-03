import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from endpoints import endpoint_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.include_router(endpoint_router)


@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "image-converter"}, status_code=200
    )
