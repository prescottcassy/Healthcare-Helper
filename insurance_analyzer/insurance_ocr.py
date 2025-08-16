import pytesseract
import cv2
import re
from typing import Dict

# Example function to extract text from image using pytesseract

def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    print("[DEBUG] OCR Extracted Text:\n", text)  # Log
    return text

# Example function to extract insurance fields from OCR text

def extract_insurance_fields(text: str) -> Dict[str, str]:
    fields = {}
    # Example regex patterns (customize as needed)
    deductible_match = re.search(r"Deductible(?: Amount)?[:\s]*\$?(\d+[,.]?\d*)", text, re.IGNORECASE)
    copay_match = re.search(r"Co[- ]?pay[:\s]*\$?(\d+[,.]?\d*)", text, re.IGNORECASE)
    coverage_match = re.search(r"Coverage[:\s]*([\w\s%]+)", text, re.IGNORECASE)
    if deductible_match:
        fields["deductible"] = deductible_match.group(1)
    if copay_match:
        fields["copay"] = copay_match.group(1)
    if coverage_match:
        fields["coverage"] = coverage_match.group(1).strip()
    return fields

# Main function to run OCR and extract fields

def analyze_insurance_card(image_path: str) -> Dict[str, str]:
    text = extract_text_from_image(image_path)
    fields = extract_insurance_fields(text)
    return fields
