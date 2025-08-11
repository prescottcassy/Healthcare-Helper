from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from module.ins_llm_loader import handle_chat_query, load_insurance_data

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    # Optionally, add more fields for user context, uploaded files, etc.


class ChatResponse(BaseModel):
    answer: str
    entities: Optional[dict] = None
    recommendations: Optional[list] = None
    coverage: Optional[list] = None
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    patient_info: Optional[dict] = None

# Load insurance data once (customize path as needed)
INSURANCE_PATH = "data/insurance.csv"
try:
    df, docs = load_insurance_data(INSURANCE_PATH)
except Exception:
    df, docs = None, None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = handle_chat_query(request.query, df, docs)
    return ChatResponse(**result)
