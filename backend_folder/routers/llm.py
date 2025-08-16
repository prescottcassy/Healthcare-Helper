from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from module import ins_llm_loader
import pandas as pd

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    symptom: Optional[str] = None
    name_input: Optional[str] = None
    file_path: Optional[str] = None
    drugs: Optional[List[str]] = None

@router.post("/load_insurance_data")
def load_insurance_data_endpoint(path: str):
    df, docs = ins_llm_loader.load_insurance_data(path)
    return {"df_shape": df.shape, "docs_count": len(docs)}

@router.post("/chunk_documents")
def chunk_documents_endpoint(docs: List[str], chunk_size: int = 300, chunk_overlap: int = 30):
    chunks = ins_llm_loader.chunk_documents(docs, chunk_size, chunk_overlap)
    return {"chunks_count": len(chunks)}

@router.post("/build_vector_db")
def build_vector_db_endpoint(chunks: List[str]):
    retriever = ins_llm_loader.build_vector_db(chunks)
    return {"retriever_type": str(type(retriever))}

@router.post("/setup_llm_chain")
def setup_llm_chain_endpoint():
    # This is a placeholder; in practice, you would pass a retriever
    return {"message": "setup_llm_chain requires a retriever object"}

@router.post("/get_drugs_for_symptom")
def get_drugs_for_symptom_endpoint(symptom: str):
    drugs = ins_llm_loader.get_drugs_for_symptom(symptom)
    return {"drugs": drugs}

@router.post("/extract_text_from_card")
def extract_text_from_card_endpoint(file: UploadFile = File(...)):
    filename = file.filename if file.filename is not None else "uploaded_file"
    with open(filename, "wb") as f:
        f.write(file.file.read())
    text = ins_llm_loader.extract_text_from_card(filename)
    return {"text": text}

@router.post("/lookup_insurance")
def lookup_insurance_endpoint(path: str, name_input: str):
    df, _ = ins_llm_loader.load_insurance_data(path)
    result = ins_llm_loader.lookup_insurance(df, name_input)
    return {"result": result}

@router.post("/match_plans_by_symptom")
def match_plans_by_symptom_endpoint(path: str, drugs: List[str]):
    df, _ = ins_llm_loader.load_insurance_data(path)
    result = ins_llm_loader.match_plans_by_symptom(df, drugs)
    return {"result": result}

@router.post("/handle_chat_query")
def handle_chat_query_endpoint(query: str, path: str):
    df, docs = ins_llm_loader.load_insurance_data(path)
    result = ins_llm_loader.handle_chat_query(query, df, docs)
    return {"result": result}
