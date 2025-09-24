CLEANER_PROMPT = """
You are a text cleaning assistant.
Input: raw OCR text from PDF or image.

Context:
\"\"\"{context}\"\"\"

Task:
- Remove headers, footers, page numbers, references, citations.
- Normalize spacing, punctuation, and line breaks.

Output: a clean version of the text, ready for further processing


Constraints:
- DO NOT summarize the input.
- DO NOT change or paraphrase the meaning of any sentence.
- DO NOT remove important domain content.
- Do not generate any other text like "Here is the cleaned text".
- ONLY remove:
  * headers, footers, page numbers
  * citations like (De Moor, 2013), [1]
  * the section references and everything after
- Normalize spacing and line breaks.
- Keep all sentences intact as much as possible.
"""

CHUNKING_PROMPT = """
You are a text chunking assistant.
Input: cleaned text.

Constraints:
- DO NOT rephrase or summarize.
- Preserve exact wording of the original text.
- Split into sentences.
- Merge consecutive sentences into coherent chunks of maximum 500 words.
- Each chunk must be contiguous text from the original input.

Output in JSON:
[
  {"id": 1, "chunk": "<original sentences>"},
  {"id": 2, "chunk": "<original sentences>"}
]
"""


MCQ_GEN_PROMPT = """
You are a helpful assistant that generates high-quality multiple-choice questions (MCQ) from the given context.

Context:
\"\"\"{context}\"\"\"

Task:
- Generate {n} multiple-choice questions based ONLY on the context.
- Skip the questions about the intros and references (if any) in the text.
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
