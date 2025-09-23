# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies (for easyocr, pillow, pymupdf, tesseract, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./src ./src
COPY ./uploads ./uploads

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["fastapi", "dev", "./src/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
