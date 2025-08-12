FROM python:3.13-slim

RUN apt-get update && apt-get install -y tesseract-ocr

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 1000

CMD ["uvicorn", "backend_folder.main:app", "--host", "0.0.0.0", "--port", "10000"]