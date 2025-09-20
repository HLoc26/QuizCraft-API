# 📘 Doc2Quiz – AI hỗ trợ tự học

Dự án này cho phép người dùng **upload tài liệu (PDF, DOCX, hình ảnh, scan)** → hệ thống sẽ:
1. **OCR / Extract text** (nếu là ảnh/PDF scan).
2. **Chia nhỏ đoạn văn bản (chunk)**.
3. **Sinh câu hỏi trắc nghiệm (MCQ)** dựa trên nội dung tài liệu với sự hỗ trợ của **Ollama + LLM (Llama3.2)**.
4. Trả về JSON chuẩn để hiển thị quiz trong frontend.

---

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI/LLM**: [Ollama](https://ollama.ai/) (chạy trong Docker, model `llama3.2`)
- **OCR**: [PyMuPDF](https://pymupdf.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/), [Pillow](https://python-pillow.org/)
- **Async**: Python `asyncio`
- **Services structure**: tách `controller` / `service` / `schemas` rõ ràng

---

## 📂 Cấu trúc thư mục

```

src/
│── main.py              # entry FastAPI
│── constants/           # hằng số (OLLAMA\_URL, prompt template…)
│── schemas/             # Pydantic request/response
│── controllers/         # FastAPI routers
│── services/            # business logic (OCR, MCQ, Upload…)
│   ├── __init__.py
│   ├── scan_service.py
│   ├── upload_service.py
│   ├── ocr_service.py
│   └── mcq_service.py
│── utils/               # helper function (TextHelper…)

````

---

## ⚙️ Cài đặt

### 1. Clone repo
```bash
git clone https://github.com/hloc26/D2Q.git
cd D2Q
````

### 2. Tạo virtualenv & cài dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Chạy Ollama trong Docker

```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull llama3.2
```

### 4. Chạy server FastAPI

```bash
uvicorn src.main:app --reload
```

Mở [http://localhost:8000/docs](http://localhost:8000/docs) để thử API.

---

## 📡 API endpoints

### Upload + OCR

```http
POST /upload
```

* Nhận file (PDF/DOCX/IMG/TXT), lưu vào server, trả về text đã extract.

### Sinh câu hỏi trắc nghiệm

```http
POST /mcq/generate
```

Body:

```json
{
  "text": "Nội dung cần sinh câu hỏi",
  "max_chunk_word": 200,
  "question_per_chunk": 3
}
```

Response:

```json
{
  "questions": [
    {
      "question": "George Washington sinh ngày nào?",
      "options": ["22 tháng 2", "22 tháng 12", "12 tháng 2", "15 tháng 2"],
      "answer": "22 tháng 2",
      "source_chunk_index": 0
    }
  ]
}
```

---

## 📝 Todo / Roadmap

* [ ] Thêm lựa chọn ngôn ngữ (Anh/Việt).
* [ ] Tối ưu sinh đáp án nhiễu hợp lý hơn.
* [ ] Thêm UI frontend để làm quiz.
* [ ] Hỗ trợ thêm model (Mistral, Gemma…).

---

## 📜 License

MIT License. Free for personal & educational use.

```

---