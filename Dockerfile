FROM python:3.13-slim

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 10000

CMD ["uvicorn", "backend_folder.main:app", "--host", "0.0.0.0", "--port", "10000"]
