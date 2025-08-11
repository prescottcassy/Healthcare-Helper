from fastapi import APIRouter, UploadFile, File
from ..services.ocr_service import extract_insurance_info

router = APIRouter()

@router.post("/upload")
async def upload_insurance(file: UploadFile = File(...)):
    contents = await file.read()
    result = extract_insurance_info(contents)
    return {"extracted_data": result}