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
    
    # Extract common insurance fields
    patterns = {
        "subscriber_name": r"Subscriber Name[:\s]*([A-Za-z .]+)",
        "subscriber_id": r"Subscriber ID[:\s]*([A-Z0-9]+)",
        "group_no": r"Group No[:\s]*([0-9]+)",
        "rxbin_group": r"RxBin/Group[:\s]*([0-9A-Z ]+)",
        "date_issued": r"Date Issued[:\s]*([0-9/]+)",
        "primary": r"Primary[:\s]*\$?([0-9]+)",
        "specialist": r"Specialist[:\s]*\$?([0-9]+)",
        "urgent_care": r"Urgent Care[:\s]*\$?([0-9]+)",
        "er": r"ER[:\s]*\$?([0-9]+)",
        "prescription_drug": r"Prescription Drug[:\s]*([\$0-9/ %\-]+)",
        "preventive_care": r"Preventive Care[:\s]*([A-Za-z ]+)",
        # Add copay and deductible patterns
        "copay": r"Copay[:\s]*\$?([0-9]+)",
        "deductible": r"Deductible[:\s]*\$?([0-9]+)",
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()

    # Enhanced extraction for copay and deductible
    # Look for '$X Copay', 'No Copay', '$X Deductible', 'No Deductible'
    copay_match = re.search(r'(\$\d+|No)\s*Copay', text, re.IGNORECASE)
    if copay_match:
        val = copay_match.group(1)
        fields['copay'] = val if val.lower() != 'no' else '0'

    deductible_match = re.search(r'(\$\d+|No)\s*Deductible', text, re.IGNORECASE)
    if deductible_match:
        val = deductible_match.group(1)
        fields['deductible'] = val if val.lower() != 'no' else '0'

    # Generic extraction for all $-amounts and copay/deductible-like fields
    dollar_fields = re.findall(r'([A-Za-z ]+?)[:\s\-]+\$([0-9]+(?:/[0-9]+)*(?:%|))', text)
    for label, value in dollar_fields:
        label_key = label.strip().lower().replace(' ', '_')
        if label_key not in fields:
            fields[label_key] = value.strip()

    # Try to extract all key-value pairs (label: value)
    key_value_pairs = re.findall(r'([A-Za-z][A-Za-z0-9 /-]+)[:\s]+([A-Za-z0-9$%/., -]+?)(?= [A-Z][a-zA-Z]+:|$)', text)
    for label, value in key_value_pairs:
        label_key = label.strip().lower().replace(' ', '_').replace('-', '_')
        if label_key not in fields and len(value.strip()) > 0:
            fields[label_key] = value.strip()
    fields["raw_text"] = text  # Add raw OCR text for debugging
    return fields

# Main function to run OCR and extract fields

def analyze_insurance_card(image_path: str) -> Dict[str, str]:
    text = extract_text_from_image(image_path)
    fields = extract_insurance_fields(text)
    return fields
