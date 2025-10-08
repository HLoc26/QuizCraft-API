# 📘 QuizCraft – AI-Powered Self Learning

This project allows users to **upload documents (PDF, DOCX, images, scans)** → the system will:  
1. **OCR / Extract text** (if the file is an image or scanned PDF).  
2. **Split text into chunks**.  
3. **Generate multiple-choice questions (MCQs)** from the content using **Ollama + LLM (Llama3.2)**.  
4. Return clean JSON so that quizzes can be displayed in a frontend.  

---

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **AI/LLM**: [Ollama](https://ollama.ai/) (running in Docker, model `llama3.2`)  
- **OCR**: [PyMuPDF](https://pymupdf.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/), [Pillow](https://python-pillow.org/)  
- **Async**: Python `asyncio`  
- **Architecture**: Clean separation of `controller` / `service` / `schemas`  

---

## 📂 Project Structure

```

src/
│── main.py              # FastAPI entry point
│── constants/           # constants (OLLAMA_URL, prompt templates…)
│── schemas/             # Pydantic request/response models
│── controllers/         # FastAPI routers
│── services/            # business logic (OCR, MCQ, Upload…)
│   ├── __init__.py
│   ├── scan_service.py
│   ├── upload_service.py
│   ├── ocr_service.py
│   └── mcq_service.py
│── utils/               # helper utilities (TextHelper…)

````

---

## ⚙️ Setup

### 1. Clone repo
```bash
git clone https://github.com/hloc26/QuizCraft-API.git
cd QuizCraft-API
````

### 2. Create virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

If you want to use your GPU, make sure you have CUDA installed, and uncomment the last line in requirements.txt 

```
# -f https://download.pytorch.org/whl/cu129 <- Uncomment this
```

### 3. Run Ollama in Docker

```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull llama3.2
```

### 4. Run FastAPI server

```bash
fastapi dev src/main.py
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to test the API.

---

## 📡 API Endpoints

### Upload + OCR

```http
POST /upload
```

* Accepts PDF/DOCX/IMG/TXT files, stores them on the server, and extracts text.

### Generate MCQs

```http
POST /mcq/generate
```

Request body:

```json
{
  "text": "Some content to generate questions from",
  "max_chunk_word": 200,
  "question_per_chunk": 3
}
```

Response:

```json
{
  "questions": [
    {
      "question": "When was George Washington born?",
      "options": ["February 22", "December 22", "February 12", "February 15"],
      "answer": "February 22",
      "source_chunk_index": 0
    }
  ]
}
```

---

## 📝 Roadmap

* [ ] Add language selection (English / Vietnamese).
* [ ] Improve distractor (wrong answers) generation.
* [ ] Add frontend UI for quizzes.
* [ ] Support more LLMs (Mistral, Gemma, etc).

---

## 📜 License

MIT License. Free for personal & educational use.
