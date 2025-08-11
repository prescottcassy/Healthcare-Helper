# healthcare-helper-backend-architecture

This is the backend API for the Healthcare Helper project. It provides services to analyze insurance plans, extract information using OCR, and help users estimate healthcare procedure costs.

## Features

- FastAPI-based backend server
- OCR service to extract insurance details from uploaded documents
- Insurance data processing and analysis endpoints
- Modular code structure with routers and services

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Tesseract OCR (if using OCR service locally)
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/saimasano123/healthcare-helper-backend-architecture.git
   cd healthcare-helper-backend-architecture
   
## Installation and Setup

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

## Install Dependencies

pip install -r requirements.txt

## Run the Backend server:

uvicorn main:app --reload

Server will start at: http://127.0.0.1:8000
