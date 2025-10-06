import asyncio
from typing import Literal, Self
from fastapi import HTTPException
from schemas.schema import GenerateRequest
from services import MCQService
from services.text_process_service import TextProcessingService
from utils.language_mapping import LanguageMapping
from utils.response_helper import ResponseHelper


class MCQController:
    def __init__(self):
        self.mcq_service = MCQService()
        self.text_processing_service = TextProcessingService()

    async def generate(self: Self, req: GenerateRequest, language: Literal["en", "vi"]):
        input_text = req.text
        # print(input_text)
        # Step 2: detect and delete headers, footers, page numbers
        pages = self.text_processing_service.remove_headers(input_text)
        # pages = input_text

        # Step 3: Chunk by tokens
        print("Splitting into chunks")
        chunks = self.text_processing_service.chunk_by_token(pages)
        print("Splitted into ", len(chunks), "chunks")

        with open("chunks.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(chunks))

        print("Min chunk length:", len(min(chunks, key=lambda x: len(x))))
        print("Max chunk length:", len(max(chunks, key=lambda x: len(x))))

        # Step 4: Clean texts
        # print("Cleaning text")
        # cleaned_texts = await asyncio.gather(*[self.text_processing_service.clean_text(chunk) for chunk in chunks])
        # print("Text cleaned")
        cleaned_texts = chunks

        # return ResponseHelper.success(
        #     data={
        #         "questions": {
        #             "question": "Miếu hiệu của Khúc Thừa Dụ là gì?",
        #             "options": ["Tiên Chủ", "Trung Chủ", "Hậu Chủ", "Tĩnh Hải Quân Tiết độ sứ"],
        #             "answer": {"index": 0, "text": "Tiên Chủ"},
        #             "source_chunk_index": 0,
        #         },
        #     }
        # )

        if not cleaned_texts:
            raise HTTPException(status_code=400, detail="Empty text")

        questions = await self.mcq_service.generate_mcq(
            cleaned_and_chunked_texts=cleaned_texts,  #
            question_per_chunk=req.question_per_chunk,
            language=LanguageMapping.map(language),
        )

        print(questions)

        questions_validated = await self.mcq_service.validate_mcq(cleaned_texts, questions)

        if len(questions_validated) < len(questions):
            print("Deleted", len(questions) - len(questions_validated), "questions")

        return ResponseHelper.success(data={"questions": questions_validated})
