FROM prescottcassy/healthcare-helper:latest


# Accept env vars
ENV OPEN_AI_KEY=""
ENV OTHER_VAR=""

CMD ["uvicorn", "backend-folder.main:app", "--host", "0.0.0.0", "--port", "8000"]

