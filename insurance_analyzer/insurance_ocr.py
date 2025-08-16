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
    # Resize for better OCR (optional, adjust as needed)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    # Clean up text
    text = text.replace('\n', ' ').replace('\r', ' ').strip()
    return text

# Example function to extract insurance fields from OCR text

def extract_insurance_fields(text: str) -> Dict[str, str]:
    fields = {}
    
    name_match = re.search(r"Subscriber Name[:\s]*([A-Za-z .]+)", text, re.IGNORECASE)
    id_match = re.search(r"Subscriber ID[:\s]*([A-Z0-9]+)", text, re.IGNORECASE)
    group_match = re.search(r"Group No[:\s]*([0-9]+)", text, re.IGNORECASE)
    rxbin_match = re.search(r"RxBin/Group[:\s]*([0-9]+)", text, re.IGNORECASE)
    date_match = re.search(r"Date Issued[:\s]*([0-9/]+)", text, re.IGNORECASE)
    primary_match = re.search(r"Primary[:\s]*\$?([0-9]+)", text, re.IGNORECASE)
    specialist_match = re.search(r"Specialist[:\s]*\$?([0-9]+)", text, re.IGNORECASE)
    urgent_match = re.search(r"Urgent Care[:\s]*\$?([0-9]+)", text, re.IGNORECASE)
    er_match = re.search(r"ER[:\s]*\$?([0-9]+)", text, re.IGNORECASE)
    rx_match = re.search(r"Prescription Drug[:\s]*([\\$0-9/ %]+)", text, re.IGNORECASE)
    preventive_match = re.search(r"Preventive Care[:\s]*([A-Za-z ]+)", text, re.IGNORECASE)

    if name_match:
        fields["subscriber_name"] = name_match.group(1).strip()
    if id_match:
        fields["subscriber_id"] = id_match.group(1).strip()
    if group_match:
        fields["group_no"] = group_match.group(1).strip()
    if rxbin_match:
        fields["rxbin_group"] = rxbin_match.group(1).strip()
    if date_match:
        fields["date_issued"] = date_match.group(1).strip()
    if primary_match:
        fields["primary"] = primary_match.group(1).strip()
    if specialist_match:
        fields["specialist"] = specialist_match.group(1).strip()
    if urgent_match:
        fields["urgent_care"] = urgent_match.group(1).strip()
    if er_match:
        fields["er"] = er_match.group(1).strip()
    if rx_match:
        fields["prescription_drug"] = rx_match.group(1).strip()
    if preventive_match:
        fields["preventive_care"] = preventive_match.group(1).strip()
    fields["raw_text"] = text  # Add raw OCR text for debugging
    return fields

# Main function to run OCR and extract fields

def analyze_insurance_card(image_path: str) -> Dict[str, str]:
    text = extract_text_from_image(image_path)
    fields = extract_insurance_fields(text)
    return fields
