from typing import List, Optional, Union, Any
from pydantic import BaseModel


# Request for /clean
class CleanRequest(BaseModel):
    chunks: List[str]


# Request for /generate
class GenerateMCQRequest(BaseModel):
    cleaned_chunks: List[str]
    question_per_chunk: int = 2
    language: str = "vi"


# Request for /validate
class ValidateMCQRequest(BaseModel):
    cleaned_chunks: List[str]
    questions: List[Any]  # hoặc có thể dùng List[MCQ] nếu chắc chắn


class PagedText(BaseModel):
    page: int
    text: str


# Send document in the request, with optional questions per chunk of text (400 word each chunk),
class GenerateRequest(BaseModel):
    text: Union[str, List[PagedText]]
    question_per_chunk: Optional[int] = 2
    max_chunk_word: Optional[int] = 400


class Answer(BaseModel):
    index: int
    text: str


# Multiple choice questions
class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: Answer
    source_chunk_index: Optional[int] = None


# Response with a list of MCQ
class GenerateResponse(BaseModel):
    questions: List[MCQ]


class ChunkQuestionMapping(BaseModel):
    chunk_index: int
    chunk_text: str
    questions: List[MCQ]


class MCQFlat(BaseModel):
    question: str
    options: list[str]
    answer_index: int
    answer_text: str
    source_chunk_index: int


VALIDATE_RESPONSE_SCHEMA_FLAT = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "option1": {"type": "string"},
            "option2": {"type": "string"},
            "option3": {"type": "string"},
            "option4": {"type": "string"},
            "answer_index": {"type": "integer"},
            "answer_text": {"type": "string"},
            "source_chunk_index": {"type": "integer"},
        },
        "required": ["question", "option1", "option2", "answer_index", "answer_text"],
    },
}
