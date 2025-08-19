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

    # Robust extraction for copay and deductible (handles line breaks, whitespace, end-of-line)
    copay_match = re.search(r'(\$\d+|No)[\s\n\r\t\-:]*Copay', text, re.IGNORECASE | re.MULTILINE)
    if not copay_match:
        copay_match = re.search(r'Copay[\s\n\r\t\-:]*([\$\d]+|No)', text, re.IGNORECASE | re.MULTILINE)
    if copay_match:
        val = copay_match.group(1)
        fields['copay'] = val if val.lower() != 'no' else '0'

    # Enhanced deductible extraction: match 'No Deductible', '$X Deductible', with any whitespace, line breaks, or OCR quirks
    deductible_match = re.search(r'(\$\d+|No)[\s\n\r\t\-:]*Deductible', text, re.IGNORECASE | re.MULTILINE)
    if not deductible_match:
        deductible_match = re.search(r'Deductible[\s\n\r\t\-:]*([\$\d]+|No)', text, re.IGNORECASE | re.MULTILINE)
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
    return fields

# Main function to run OCR and extract fields


def format_insurance_data(cleaned: Dict[str, str]) -> str:
    # Helper functions
    def beautify_key(key):
        return key.replace('_', ' ').title()
    def beautify_value(val):
        if isinstance(val, str):
            return ' '.join([w.capitalize() if w.isalpha() else w for w in val.split()])
        return val

    # Section fields
    member_info = []
    coverage = []
    drug_coverage = []
    notes = []

    # Member Information
    if 'subscriber_name' in cleaned:
        member_info.append(f"<li><b>Name:</b> {beautify_value(cleaned['subscriber_name'])}</li>")
    if 'subscriber_id' in cleaned:
        member_info.append(f"<li><b>Subscriber ID:</b> {beautify_value(cleaned['subscriber_id'])}</li>")
    if 'group' in cleaned:
        member_info.append(f"<li><b>Group:</b> {beautify_value(cleaned['group'])}</li>")
    if 'date_issued' in cleaned:
        member_info.append(f"<li><b>Date Issued:</b> {beautify_value(cleaned['date_issued'])}</li>")
    if 'rxbin_group' in cleaned:
        member_info.append(f"<li><b>RxBIN/Group:</b> {beautify_value(cleaned['rxbin_group'])}</li>")

    # Coverage & Benefits
    if 'primary' in cleaned:
        coverage.append(f"<li><b>Primary Care Visit:</b> ${beautify_value(cleaned['primary'])}</li>")
    if 'specialist' in cleaned:
        coverage.append(f"<li><b>Specialist Visit:</b> ${beautify_value(cleaned['specialist'])}</li>")
    if 'urgent_care' in cleaned:
        coverage.append(f"<li><b>Urgent Care:</b> ${beautify_value(cleaned['urgent_care'])}</li>")
    if 'er' in cleaned:
        coverage.append(f"<li><b>Emergency Room (ER):</b> ${beautify_value(cleaned['er'])}</li>")
    if 'preventive_care' in cleaned:
        coverage.append(f"<li><b>Preventive Care:</b> {beautify_value(cleaned['preventive_care'])}</li>")

    # Prescription Drug Coverage
    if 'prescription_drug' in cleaned:
        drug_coverage.append(f"<li><b>Prescription Drug:</b> {beautify_value(cleaned['prescription_drug'])}</li>")
    if 'copay' in cleaned:
        drug_coverage.append(f"<li><b>Copay:</b> ${beautify_value(cleaned['copay'])}</li>")
    if 'deductible' in cleaned:
        drug_coverage.append(f"<li><b>Deductible:</b> ${beautify_value(cleaned['deductible'])}</li>")

    # Notes
    if 'members' in cleaned:
        notes.append(f"<li>Member: <b>{beautify_value(cleaned['members'])}</b></li>")
    if 'responsibility' in cleaned:
        notes.append(f"<li>{beautify_value(cleaned['responsibility'])}</li>")

    html = ""
    if member_info:
        html += "<b>Member Information</b><ul>" + ''.join(member_info) + "</ul>"
    if coverage:
        html += "<hr><b>Coverage & Benefits</b><ul>" + ''.join(coverage) + "</ul>"
    if drug_coverage:
        html += "<hr><b>Prescription Drug Coverage</b><ul>" + ''.join(drug_coverage) + "</ul>"
    if notes:
        html += "<hr><b>Notes</b><ul>" + ''.join(notes) + "</ul>"
    return html

def analyze_insurance_card(image_path: str) -> dict:
    text = extract_text_from_image(image_path)
    fields = extract_insurance_fields(text)

    # Remove raw_text and null-like entries
    cleaned = {k: v for k, v in fields.items() if k != "raw_text" and v not in ["", "null", None]}
    # sort keys for consistent output
    cleaned = dict(sorted(cleaned.items()))
    summary = format_insurance_data(cleaned)
    return {"fields": cleaned, "summary": summary}

