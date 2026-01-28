from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

REGISTRY_FILE = "backend/registry/letter_registry.xlsx"


@router.get("/download/excel")
def download_excel():
    if not os.path.exists(REGISTRY_FILE):
        raise HTTPException(status_code=404, detail="Registry not found")

    return FileResponse(
        path=REGISTRY_FILE,
        filename="letter_registry.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
