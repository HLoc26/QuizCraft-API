import os

from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "uploads"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GENERATIVE_PROVIDER = os.getenv("GENERATIVE_PROVIDER", "gemini")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
