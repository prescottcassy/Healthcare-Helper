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
    # For now, create a sample patient with insurance. You can expand this to use user data.
    patient = assistant.create_sample_patient(has_insurance=True)
    # Process the user's query
    result = assistant.process_query(request.text, patient)
    # Return the full result as a dict
    return EntitiesResponse(response=result)
