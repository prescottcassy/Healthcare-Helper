# --- CMS Provider Data Integration ---

# Use relative import for cms_ingestion
import os
import sys
cms_ingest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_ingestion/module/cms_ingestion'))
if cms_ingest_path not in sys.path:
    sys.path.append(cms_ingest_path)
try:
    from data_ingestion.module.cms_ingestion.cms_ingestion import fetch_cms_data
except ImportError:
    fetch_cms_data = None
# Helper to wire extracted card fields to chat handler
def answer_from_card_fields(query: str, card_fields: dict):
    """
    Call handle_chat_query with only card_fields for direct Q&A from insurance card extraction.
    """
    return handle_chat_query(query, card_fields=card_fields)

# Example usage (for integration in API):
# extracted_fields = {"copay": "25", "subscriber_name": "John Doe"}
# user_query = "What is my copay?"
# result = answer_from_card_fields(user_query, extracted_fields)
# print(result["answer"])  # -> Your copay is 25

# Cache CMS data at module load (can be improved for production)
cms_provider_df = None
if fetch_cms_data:
    try:
        cms_provider_df = fetch_cms_data()
    except Exception as e:
        cms_provider_df = None

def search_cms_providers(query: str):
    """Search CMS provider data for a provider name or specialty."""
    if cms_provider_df is None or len(cms_provider_df) == 0:
        return []
    q = query.lower()
    # Try to match provider name or specialty columns
    results = cms_provider_df[cms_provider_df.apply(lambda row: q in str(row).lower(), axis=1)]
    return results.to_dict(orient="records")[:5]  # Return top 5 matches
# insurance_llm_loader.py

import os
import pandas as pd
import requests
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

openai_api_key = os.getenv("OPENAI_API_KEY")

def load_insurance_data(path: str):
    df = pd.read_csv(path)
    loader = CSVLoader(file_path=path)
    docs = loader.load()
    return df, docs

def chunk_documents(docs, chunk_size=300, chunk_overlap=30):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

def build_vector_db(chunks):
    embedding = OpenAIEmbeddings()
    db = Chroma.from_documents(chunks, embedding)
    return db.as_retriever(search_kwargs={"k": 3})

def setup_llm_chain(retriever):
    llm = ChatOpenAI(temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def get_drugs_for_symptom(symptom: str):
    url = "https://api.fda.gov/drug/drugsfda.json"
    params = {"search": f"products.active_ingredient:{symptom}", "limit": 10}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "results" in data:
            return [item["products"][0]["brand_name"].lower() for item in data["results"]]
    except:
        pass
    return []

def extract_text_from_card(file_path: str):
    if file_path.endswith(".pdf"):
        images = convert_from_path(file_path)
        return "\n".join([pytesseract.image_to_string(img) for img in images])
    else:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

def lookup_insurance(df, name_input: str):
    name_input = name_input.lower()
    matches = df[
        df["COMPANY NAME"].str.lower().str.contains(name_input) |
        df["PLAN NAME"].str.lower().str.contains(name_input)
    ]
    return matches

def match_plans_by_symptom(df, drugs):
    if not drugs:
        return pd.DataFrame()
    return df[df["COVERAGE"].str.lower().str.contains('|'.join(drugs))]

# Optional: Add a main() function for CLI or script usage

# Chat handler for routing user queries
def handle_chat_query(query: str, df=None, docs=None, card_fields=None):
    """
    Routes user queries to the appropriate function and returns a rich structured response.
    Args:
        query (str): The user's question or request.
        df (pd.DataFrame): Insurance dataframe (optional, for insurance queries).
        docs: Insurance docs (optional, for retrieval QA).
        card_fields (dict): Extracted insurance card fields (optional, for direct Q&A).
    Returns:
        dict: Rich chat response with entities, recommendations, coverage, extracted text, confidence, etc.
    """
    query_lower = query.lower()
    response = {
        "answer": None,
        "entities": {},
        "recommendations": [],
        "coverage": None,
        "extracted_text": None,
        "confidence": 1.0,
        "patient_info": None
    }

    # --- Direct Q&A from insurance card fields ---
    if card_fields is not None and isinstance(card_fields, dict):
        # Simple keyword matching for common insurance fields
        for key in card_fields:
            if key in query_lower or key.replace('_', ' ') in query_lower:
                response["answer"] = f"{key.replace('_', ' ').title()}: {card_fields[key]}"
                response["confidence"] = 1.0
                return response
        # Special handling for copay, deductible, etc.
        for field in ["copay", "deductible", "primary", "specialist", "urgent_care", "er"]:
            if field in query_lower and field in card_fields:
                response["answer"] = f"Your {field.replace('_', ' ')} is {card_fields[field]}"
                response["confidence"] = 1.0
                return response

    # --- CMS Provider Data Q&A ---
    if ("medicare" in query_lower or "cms" in query_lower or "provider" in query_lower) and fetch_cms_data:
        providers = search_cms_providers(query)
        if providers:
            response["answer"] = f"Found {len(providers)} Medicare providers for your query."
            response["coverage"] = providers
        else:
            response["answer"] = "No Medicare providers found for your query."
        return response

    # Drug suggestion based on symptom
    if "drug" in query_lower or "medicine" in query_lower or "symptom" in query_lower:
        for word in ["for ", "with ", "about ", "symptom "]:
            if word in query_lower:
                symptom = query_lower.split(word)[-1].split()[0]
                drugs = get_drugs_for_symptom(symptom)
                response["entities"]["symptom"] = symptom
                response["recommendations"] = drugs
                if drugs:
                    response["answer"] = f"Suggested drugs for '{symptom}': {', '.join(drugs)}"
                else:
                    response["answer"] = f"No drug suggestions found for '{symptom}'."
                return response
        response["answer"] = "Please specify a symptom to get drug suggestions."
        return response
    # Insurance lookup
    elif "insurance" in query_lower or "plan" in query_lower:
        if df is not None:
            for word in ["for ", "named ", "plan "]:
                if word in query_lower:
                    name = query_lower.split(word)[-1].split()[0]
                    matches = lookup_insurance(df, name)
                    response["entities"]["plan_name"] = name
                    if not matches.empty:
                        response["coverage"] = matches.to_dict(orient="records")
                        response["answer"] = f"Insurance plans matching '{name}':"
                    else:
                        response["answer"] = f"No insurance plans found for '{name}'."
                    return response
        response["answer"] = "Please specify an insurance company or plan name."
        return response
    # Insurance card extraction
    elif "card" in query_lower or "extract" in query_lower:
        response["answer"] = "Please upload your insurance card image or PDF for extraction."
        return response
    # Plan coverage by drug
    elif "cover" in query_lower or "coverage" in query_lower:
        if df is not None:
            for word in ["for ", "of ", "drug "]:
                if word in query_lower:
                    drug = query_lower.split(word)[-1].split()[0]
                    plans = match_plans_by_symptom(df, [drug])
                    response["entities"]["drug"] = drug
                    if not plans.empty:
                        response["coverage"] = plans.to_dict(orient="records")
                        response["answer"] = f"Plans covering '{drug}':"
                    else:
                        response["answer"] = f"No plans found covering '{drug}'."
                    return response
        response["answer"] = "Please specify a drug name to check coverage."
        return response
    # Retrieval QA (general question)
    elif docs is not None:
        chunks = chunk_documents(docs)
        retriever = build_vector_db(chunks)
        qa_chain = setup_llm_chain(retriever)
        answer = qa_chain.run(query)
        response["answer"] = answer
        return response
    else:
        response["answer"] = "Sorry, I couldn't understand your request. Please ask about drugs, insurance, upload a card, or ask about Medicare providers."
        response["confidence"] = 0.5
        return response
