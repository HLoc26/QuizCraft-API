from typing import Literal, Self
from fastapi import HTTPException
from schemas.request import GenerateRequest
from services import MCQService
from utils import TextHelper
from utils.language_mapping import LanguageMapping


class MCQController:
    def __init__(self):
        self.mcq_service = MCQService()

    async def generate(self: Self, req: GenerateRequest, language: Literal["en", "vi"]):
        text = TextHelper.clean_text(req.text)
        if not text:
            raise HTTPException(status_code=400, detail="Empty text")

        questions = await self.mcq_service.generate_mcq(
            text=text,  #
            max_chunk_word=req.max_chunk_word,
            question_per_chunk=req.question_per_chunk,
            language=LanguageMapping.map(language),
        )
        return {"questions": questions}
