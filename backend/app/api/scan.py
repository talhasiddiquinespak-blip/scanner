from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import os

from backend.services.ocr_service import extract_text_from_image
from backend.services.ai_parser import extract_letter_fields
from backend.utils.excel_registry import append_letter_record

router = APIRouter()

SCANS_DIR = "backend/scans"

if not os.path.exists(SCANS_DIR):
    os.makedirs(SCANS_DIR)


@router.post("/scan")
async def scan_letter(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    try:
        image_bytes = await file.read()

        # Save scanned image
        file_id = str(uuid4())
        file_name = f"{file_id}.jpg"
        file_path = os.path.join(SCANS_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # OCR
        extracted_text = extract_text_from_image(image_bytes)

        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text detected in image")

        # AI Parsing
        extracted_fields = extract_letter_fields(extracted_text)

        # Excel Update
        append_letter_record(extracted_fields, file_name)

        return {
            "status": "success",
            "data": extracted_fields
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

