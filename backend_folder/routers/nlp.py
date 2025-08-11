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
    parse_data: Optional[dict] = None  # Data fetched from Parse

@router.post("/query", response_model=EntitiesResponse)
async def extract_entities(request: QueryRequest):
    assistant = HealthcareAIAssistant()
    # Fetch data from Back4app (Parse)
    parse_data = assistant.get_data_from_parse()
    # Create a sample patient and process the query
    patient = assistant.create_sample_patient(has_insurance=True)
    result = assistant.process_query(request.text, patient)
    # Return both the processed result and the parse data
    return EntitiesResponse(
        response=result,
        patient_info=parse_data,
        parse_data=parse_data
    )