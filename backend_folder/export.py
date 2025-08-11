import json
from typing import List, Dict

def export_to_json(data: List[Dict], output_path: str):
    """Writes embedded chunks to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
