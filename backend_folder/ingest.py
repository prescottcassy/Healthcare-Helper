from typing import List

def ingest_documents(input_path: str) -> List[str]:
    """Reads text files from a directory and returns a list of raw strings."""
    import os

    docs = []
    for filename in os.listdir(input_path):
        if filename.endswith(".txt"):
            with open(os.path.join(input_path, filename), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs
