import asyncio
from typing import List
from ..clients.ai_client import AIClient
from ..constants import MCQ_GEN_PROMPT, GENERATIVE_PROVIDER, VALIDATE_PROMPT
from ..schemas import MCQ, ChunkQuestionMapping


class MCQService:
    def __init__(self):
        # provider chọn từ .env
        self.client = AIClient.get_instance(provider=GENERATIVE_PROVIDER)

    async def generate_mcq(self, cleaned_and_chunked_texts: List[str], question_per_chunk: int, language: str) -> List[MCQ]:
        questions: List[MCQ] = []

        async def gen_for_chunk(idx, chunk):
            prompt = MCQ_GEN_PROMPT.format(context=chunk, n=question_per_chunk, language=language)
            resp = None
            try:
                resp = await self.client.chat_structured(content=prompt, response_schema=list[MCQ])
                # print(resp)
            except Exception as e:
                print(f"Chat API error chunk {idx}: {e}")
                raise e

            if not resp:
                return []

            out: List[MCQ] = []
            for it in resp:
                # Hỗ trợ cả dạng object (Gemini) và dict (Local)
                q = it.get("question") if isinstance(it, dict) else getattr(it, "question", None)
                opts = it.get("options") if isinstance(it, dict) else getattr(it, "options", None)
                ans = it.get("answer") if isinstance(it, dict) else getattr(it, "answer", None)

                if q and opts and ans:
                    out.append(
                        MCQ(
                            question=q,
                            options=opts,
                            answer=ans,
                            source_chunk_index=idx,
                        )
                    )
            return out

        sem = asyncio.Semaphore(3)

        async def sem_task(i, c):
            async with sem:
                return await gen_for_chunk(i, c)

        results = await asyncio.gather(*[sem_task(i, c) for i, c in enumerate(cleaned_and_chunked_texts)])
        for r in results:
            questions.extend(r)

        return questions

    async def validate_mcq(self, cleaned_and_chunked_texts: List[str], questions: List[MCQ]):
        # Group theo chunk
        questions.sort(key=lambda q: q.source_chunk_index)
        chunks: List[ChunkQuestionMapping] = []
        selected: List[MCQ] = []

        for q in questions:
            if not selected:
                selected.append(q)
                continue
            if q.source_chunk_index != selected[-1].source_chunk_index:
                chunks.append(
                    ChunkQuestionMapping(
                        chunk_index=selected[-1].source_chunk_index,
                        chunk_text=cleaned_and_chunked_texts[selected[-1].source_chunk_index],
                        questions=selected,
                    )
                )
                selected = [q]
            else:
                selected.append(q)
        if selected:
            chunks.append(
                ChunkQuestionMapping(
                    chunk_index=selected[-1].source_chunk_index,
                    chunk_text=cleaned_and_chunked_texts[selected[-1].source_chunk_index],
                    questions=selected,
                )
            )

        async def validate_chunk(chunk: ChunkQuestionMapping):
            prompt = VALIDATE_PROMPT.format(
                chunk_text=chunk.chunk_text,
                questions=[q.model_dump() for q in chunk.questions],
            )
            try:
                resp = await self.client.chat_structured(prompt, response_schema=list[MCQ])
            except Exception as e:
                print(f"[validate_chunk] Error: {e}")
                raise e

            if not resp:
                return []

            out: List[MCQ] = []
            for it in resp:
                # Hỗ trợ cả dạng object (Gemini) và dict (Local)
                q = it.get("question") if isinstance(it, dict) else getattr(it, "question", None)
                opts = it.get("options") if isinstance(it, dict) else getattr(it, "options", None)
                ans = it.get("answer") if isinstance(it, dict) else getattr(it, "answer", None)

                if q and opts and ans:
                    out.append(
                        MCQ(
                            question=q,
                            options=opts,
                            answer=ans,
                            source_chunk_index=chunk.chunk_index,
                        )
                    )
            return out

        results = await asyncio.gather(*(validate_chunk(c) for c in chunks))
        validated_questions: List[MCQ] = [q for chunk_result in results for q in chunk_result]

        return validated_questions
