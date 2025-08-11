from typing import List

def chunk_documents(docs: List[str], chunk_size: int = 500) -> List[str]:
    """Splits each document into chunks of approximately `chunk_size` characters."""
    chunks = []
    for doc in docs:
        for i in range(0, len(doc), chunk_size):
            chunks.append(doc[i:i+chunk_size])
    return chunks
