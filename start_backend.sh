#!/bin/bash
# This script starts the FastAPI backend using Uvicorn from the project root

export $(grep -v '^#' .env | xargs)  # Load environment variables from .env
uvicorn backend_folder.main:app --host 0.0.0.0 --port 10000
