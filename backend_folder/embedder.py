from typing import List, Dict

def embed_chunks(chunks: List[str]) -> List[Dict]:
    """Returns dummy embeddings for each chunk (replace with real model later)."""
    embedded = []
    for i, chunk in enumerate(chunks):
        embedded.append({
            "id": i,
            "text": chunk,
            "embedding": [0.0] * 768  # Placeholder vector
        })
    return embedded
