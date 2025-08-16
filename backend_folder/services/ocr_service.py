import tempfile
from backend_folder.insurance_analyzer import insurance_ocr

def extract_insurance_info(file_bytes: bytes) -> dict:
    """Extract insurance info from uploaded image file using insurance_ocr module"""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        result = insurance_ocr.analyze_insurance_card(tmp.name)
        return result
    