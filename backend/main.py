import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from endpoints import endpoint_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.include_router(endpoint_router)

app.add_middleware(
    CORSMiddleware,
    # 1. Only origins (URLs) go here
    allow_origins=[
        "http://localhost:5173",  # Local Vite dev server
        "https://makeitdone-frontend.onrender.com",  # Your live Render site
    ],
    allow_credentials=True,
    # 2. Methods are HTTP actions, NOT URLs
    allow_methods=["*"],
    # 3. Headers are metadata, NOT URLs
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "converter_api"}, status_code=200
    )
