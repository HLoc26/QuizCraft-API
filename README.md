# QuizCraft – AI-Powered Self Learning

> This is the API repository. Check [QuizCraft-UI](https://github.com/HLoc26/QuizCraft-UI) for UI


This project allows users to **upload documents (PDF, DOCX, images, scans)** → the system will:  
1. **OCR / Extract text** (if the file is an image or scanned PDF).  
2. **Split text into chunks**.  
3. **Generate multiple-choice questions (MCQs)** from the content using **Ollama + LLM (Llama3.2)**.  
4. Return clean JSON so that quizzes can be displayed in a frontend.  

---

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **AI/LLM**: [Ollama](https://ollama.ai/) (running in Docker, model `llama3.2`)  
- **OCR**: [PyMuPDF](https://pymupdf.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/), [Pillow](https://python-pillow.org/)  
- **Async**: Python `asyncio`  
- **Architecture**: Clean separation of `controller` / `service` / `schemas`  

---

## Project Structure

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

## Setup

### 1. Clone repo
```bash
git clone https://github.com/hloc26/QuizCraft-API.git
cd QuizCraft-API
```

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

### 3. AI Model Selection & Provider Setup
You can choose which AI model and provider to use for generating quizzes. The backend supports both local (Ollama) and Google Gemini models.

#### Change Provider and Model in `.env`

Edit your `.env` file (or `.env.example` for reference):

```
GENERATIVE_PROVIDER="local"      # Use Ollama (default)
OLLAMA_MODEL="llama3.2"          # Model name for Ollama
OLLAMA_URL=http://localhost:11434 # Ollama server URL

# Or use Gemini:
GENERATIVE_PROVIDER="gemini"     # Use Google Gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL="gemini-2.5-flash"  # Model name for Gemini
```

**To switch to Gemini:**
1. Set `GENERATIVE_PROVIDER="gemini"` in your `.env`.
2. Set `GEMINI_API_KEY` to your Gemini API key (see below).
3. Optionally, change `GEMINI_MODEL` to your preferred Gemini model.

**To use Ollama (local):**
1. Set `GENERATIVE_PROVIDER="local"`.
2. Make sure `OLLAMA_URL` and `OLLAMA_MODEL` are set correctly.

#### Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in with your Google account.
2. Click "Create API Key" and copy the generated key.
3. Paste it into your `.env` file as `GEMINI_API_KEY`.

**Note:** Gemini API access may require joining a waitlist or having a Google Cloud account, depending on your region and usage.


### 4. Run Ollama in Docker

```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull llama3.2
```

### 5. Run FastAPI server

```bash
fastapi dev src/main.py
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to test the API.

---

## API Endpoints


### `POST /upload`
**Description:** Upload a file (PDF, DOCX, image, TXT) to the server. Automatically performs OCR if needed and extracts text.

**Request:**
- `multipart/form-data` with file field named `file`

**Response:**
```json
{
  "success": true,
  "data": {
    "filename": "G.W.txt",
    "text": "Extracted text from file..."
  },
  "error": null
}
```

---

### `POST /mcq/generate`
**Description:** Generate multiple-choice questions (MCQs) from provided text using LLM (Llama3.2).

**Request:**
```json
{
  "text": "Some content to generate questions from",
  "max_chunk_word": 200,
  "question_per_chunk": 3
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "questions": [
      {
        "question": "When was George Washington born?",
        "options": ["February 22", "December 22", "February 12", "February 15"],
        "answer": "February 22",
        "source_chunk_index": 0
      }
    ]
  },
  "error": null
}
```

---

### `GET /files/list`
**Description:** List all uploaded files available on the server.

**Response:**
```json
{
  "success": true,
  "data": [
    "G.W.txt",
    "Welcome.md"
  ],
  "error": null
}
```

---

### `GET /files/text?filename=...`
**Description:** Get the extracted text content of a specific uploaded file.

**Response:**
```json
{
  "success": true,
  "data": {
    "filename": "G.W.txt",
    "text": "Extracted text from file..."
  },
  "error": null
}
```

---

### `POST /mcq/scan`
**Description:** Upload a scan/image and generate MCQs directly from the scanned content (OCR + MCQ in one step).

**Request:**
- `multipart/form-data` with file field named `file`
- Optional JSON body for MCQ parameters

**Response:**
```json
{
  "success": true,
  "data": {
    "questions": [ ... ]
  },
  "error": null
}
```

---

### Error Response Format
All endpoints return errors in a consistent format:
```json
{
  "success": false,
  "data": null,
  "error": "Error message here"
}
```

---

## Roadmap

* [x] Add language selection (English / Vietnamese).
* [ ] Improve distractor (wrong answers) generation.
* [ ] Improve questions quality.
* [x] Add frontend UI for quizzes.
* [x] Support more LLMs (Mistral, Gemma, etc).

---

## License

MIT License. Free for personal & educational use.
