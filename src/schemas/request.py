from typing import List, Optional
from pydantic import BaseModel


# Send document in the request, with optional questions per chunk of text (400 word each chunk),
class GenerateRequest(BaseModel):
    text: str
    question_per_chunk: Optional[int] = 2
    max_chunk_word: Optional[int] = 400


# Multiple choice questions
class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str
    source_chunk_index: Optional[int] = None


# Response with a list of MCQ
class GenerateResponse(BaseModel):
    questions: List[MCQ]
