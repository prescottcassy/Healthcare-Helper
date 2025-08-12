from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend_folder.routers import insurance, nlp, chat
import os

from dotenv import load_dotenv
load_dotenv()  # <-- Add this line to load .env variables

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

if not OPEN_AI_KEY:
    raise ValueError("Missing OPEN_AI_KEY environment variable")

app = FastAPI(
    title="Healthcare AI Assistant Backend",
    description="API backend for insurance analysis and cost comparison",
    version="1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://prescottcassy.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],  # Allow GitHub Pages and local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insurance.router, prefix="/api/insurance", tags=["Insurance"])
app.include_router(nlp.router, prefix="/api/nlp", tags=["NLP"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Backend is working!"}