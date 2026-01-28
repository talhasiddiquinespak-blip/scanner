from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.scan import router as scan_router
from app.api.download import router as download_router

app = FastAPI(
    title="Letter Scanner System",
    version="1.0.0",
    description="Scan letters, extract data using OCR + Gemini AI, update Excel automatically"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="backend/app/static", html=True), name="static")

app.include_router(scan_router)
app.include_router(download_router)
