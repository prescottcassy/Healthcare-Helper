# routers/nlp.py


from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from module.rag_cost_recomm import HealthcareAIAssistant

router = APIRouter()

class QueryRequest(BaseModel):
    text: str


class EntitiesResponse(BaseModel):
    response: dict
    entities: Optional[dict] = None  # Extracted entities from the query
    recommendations: Optional[list] = None  # Any recommendations provided
    confidence: Optional[float] = None  # Confidence score of the extraction
    patient_info: Optional[dict] = None  # Info about the patient used in processing


@router.post("/query", response_model=EntitiesResponse)
async def extract_entities(request: QueryRequest):
    # Initialize the Healthcare AI Assistant
    assistant = HealthcareAIAssistant()
    # Fetch data from Back4app (Parse) and return it to the frontend
    parse_data = assistant.get_data_from_parse()
    return EntitiesResponse(response=parse_data)
