import pytesseract
from PIL import Image
import io

def extract_insurance_info(file_bytes: bytes) -> dict:
    """Extract insurance info from uploaded image file"""
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)

    # TODO: Add your regex extraction logic here
    extracted_data = {
        "raw_text": text,
        "deductible": None,
        "copay": None
    }
    return extracted_data
