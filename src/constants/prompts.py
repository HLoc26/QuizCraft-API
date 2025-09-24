MCQ_GEN_PROMPT = """
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
    "question": "...?",
    "options": ["opt1", "opt2", "opt3", "opt4"],
    "answer": {{ "index": 0, "text": "opt1" }}
  }},
  ...
]

Constraints:
- Each "question" must be either:
  1. A clear question ending with a question mark (?), OR
  2. A fill-in-the-blank statement with exactly one blank written as "____".
- Do not output pure declarative statements without "?" or "____".
- Do not invent facts not present in the context.
- Do not generate options characters like "A.", "B.", etc.
- Keep questions concise (one sentence) and answers short.
- The "answer.index" must always be the integer index of the correct option (0-based).
- The "answer.text" must always be copied verbatim from the correct option string.
- The entire output (except the keys) must be in {language}.
"""
