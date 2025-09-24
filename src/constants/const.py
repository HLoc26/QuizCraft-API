import os


UPLOAD_FOLDER = "uploads"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
