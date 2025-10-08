CLEANER_PROMPT = """
You are a text cleaning assistant.
Input: raw OCR text from PDF or image.

Context:
\"\"\"{context}\"\"\"

Task:
- Remove headers, footers, page numbers, references, citations.
- Normalize spacing, punctuation, and line breaks.

Output: a cleaned version of the text, ready for further processing


Constraints:
- DO NOT summarize the input.
- DO NOT return code, regex, or instructions.
- DO NOT change or paraphrase the meaning of any sentence.
- DO NOT remove important domain content.
- Do not generate any other text like "Here is the cleaned text".
- ONLY remove:
  * headers, footers, page numbers
  * citations like (De Moor, 2013), [1]
  * the section references and everything after
- Normalize spacing and line breaks.
- Keep all sentences intact as much as possible.
- MUST return the cleaned text directly.
- No empty output.
- If nothing needs to be cleaned, return the original text.
"""

MCQ_GEN_PROMPT = """
You are an assistant that generates high-quality multiple-choice questions (MCQs) from the given context.

Context:
\"\"\"{context}\"\"\"

Task:
- Generate {n} multiple-choice questions based ONLY on the given context.
- Skip questions about introductions, references, acknowledgments, or unrelated meta-text.
- Each question must have exactly 4 options.
- Mark which option is correct.
- Distractors must be plausible: 
  * grammatically consistent with the correct answer,
  * semantically related to the topic,
  * but clearly incorrect if compared carefully with the context.
- Ensure variety: 
  * Avoid repeating similar questions or answers.
- Do not generate any text outside the JSON array.

Output Format:
- MUST be valid JSON array:
[
  {{
    "question": "...?",
    "options": ["opt1", "opt2", "opt3", "opt4"],
    "answer": {{ "index": 0, "text": "opt1" }}
  }},
  ...
]

Constraints:
- Do not return any text or code block other than the JSON array,
- Each "question" must be either:
  1. A clear question ending with "?", OR
  2. A fill-in-the-blank with exactly one blank "____".
- Do not output plain declarative statements without "?" or "____".
- Do not invent facts not present in the context.
- Do not label options with "A.", "B.", etc. — options must be plain strings.
- Keep questions concise (one sentence) and answers short.
- "answer.index" must always be the 0-based integer index of the correct option.
- "answer.text" must be copied verbatim from the correct option string.
- The entire output (except the JSON keys) must be in {language}.
"""

VALIDATE_PROMPT = """
You are a helpful assistant that validates multiple-choice questions (MCQs) against the provided source text.

Source text:
\"\"\"{chunk_text}\"\"\"

MCQs to validate:
{questions}

Validation task:
- Only return the improved list of MCQs, nothing else.
- Remove MCQs that:
  * are not supported by the source text,
  * are too trivial (e.g., the correct answer is explicitly copied into the question statement),
  * are unnatural or nonsensical,
  * have duplicate meaning or are redundant.
- Ensure each remaining MCQ:
  * is clearly based on the source text,
  * has exactly 1 correct option,
  * has 3 plausible distractors that are not obviously wrong,
  * is phrased naturally and clearly.

Output format:
- Return only the cleaned list of MCQs, with the same structure as input.
"""
