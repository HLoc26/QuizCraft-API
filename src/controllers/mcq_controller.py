from typing import Literal
from fastapi import HTTPException
from ..schemas import GenerateRequest
from ..services import MCQService, TextProcessingService
from ..utils import LanguageMapping, ResponseHelper


class MCQController:
    def __init__(self):
        self.mcq_service = MCQService()
        self.text_processing_service = TextProcessingService()

    async def chunk(self, req: GenerateRequest):
        input_text = req.text
        # Bước 1: Xử lý header/footer
        pages = self.text_processing_service.remove_headers(input_text)
        # Bước 2: Chunk
        chunks = self.text_processing_service.chunk_by_token(pages)
        return ResponseHelper.success(data={"num_chunks": len(chunks), "chunks": chunks})

    async def clean(self, chunks: list[str]):
        # Bước 3: Clean từng chunk (có thể async nếu clean_text là async)
        # cleaned_chunks = await asyncio.gather(*[self.text_processing_service.clean_text(chunk) for chunk in chunks])
        cleaned_chunks = chunks  # Nếu chưa có clean thực sự
        return ResponseHelper.success(data={"success": True, "cleaned_chunks": cleaned_chunks})

    async def generate(self, cleaned_chunks: list[str], question_per_chunk: int, language: Literal["en", "vi"]):
        if not cleaned_chunks:
            raise HTTPException(status_code=400, detail="Empty text")
        questions = await self.mcq_service.generate_mcq(
            cleaned_and_chunked_texts=cleaned_chunks,
            question_per_chunk=question_per_chunk,
            language=LanguageMapping.map(language),
        )
        return ResponseHelper.success(data={"questions": questions})

    async def validate(self, cleaned_chunks: list[str], questions: list):
        questions_validated = await self.mcq_service.validate_mcq(cleaned_chunks, questions)
        return ResponseHelper.success(data={"questions": questions_validated})
