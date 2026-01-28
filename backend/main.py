from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api.scan import router as scan_router
from backend.app.api.download import router as download_router

app = FastAPI(
    title="Letter Scanner System",
    version="1.0.0",
    description="Scan letters, extract data using OCR + Gemini AI, update Excel automatically"
)

# CORS (safe for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="backend/app/static", html=True),
    name="static",
)

# API routes
app.include_router(scan_router, prefix="/api")
app.include_router(download_router, prefix="/api")

