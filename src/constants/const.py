import os


UPLOAD_FOLDER = "uploads"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

PROMPT_TEMPLATE = """
You are a helpful assistant that generates high-quality multiple-choice questions (MCQ) from the given context.

Context:
\"\"\"{context}\"\"\"

Task:
- Generate {n} multiple-choice questions based ONLY on the context.
- Each question must have exactly 4 options.
- Mark which option is correct.
- Distractors should be plausible and not obviously incorrect.
- Do not generate any other text like "Here are the questions".
- Output MUST be valid JSON array like:
[
  {{
    "question": "...",
    "options": ["opt1", "opt2", "opt3", "opt4"],
    "answer": "opt1"
  }},
  ...
]

Constraints:
- Do not invent facts not present in the context.
- Keep questions concise (one sentence) and answers short.
"""
