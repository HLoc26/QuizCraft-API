import asyncio
import json
import re
from typing import List
from ollama import AsyncClient
from constants import OLLAMA_MODEL, OLLAMA_URL, MCQ_GEN_PROMPT
from schemas import MCQ
from utils import TextHelper


class MCQService:
    def __init__(self):
        self.client = AsyncClient(host=OLLAMA_URL)

    async def generate_mcq(self, text: str, max_chunk_word: int, question_per_chunk: int, language: str) -> List[MCQ]:
        chunks = TextHelper.chunk_text_by_word(text, max_words=max_chunk_word)
        print("chunks:", chunks)
        questions = []

        async def gen_for_chunk(idx, chunk):
            prompt = MCQ_GEN_PROMPT.format(context=chunk, n=question_per_chunk, language=language)
            text_out = None

            # Try chat API
            try:
                resp = await self.client.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}], stream=False)
                text_out = resp["message"]["content"]
            except Exception as e:
                print(f"Chat API error chunk {idx}: {e}")
                try:
                    resp = await self.client.generate(model="llama3.2", prompt=prompt)
                    text_out = resp["response"]
                except Exception as e2:
                    print(f"Generate API error chunk {idx}: {e2}")

            if not text_out:
                return []

            # Parse JSON
            try:
                data = json.loads(text_out)
            except json.JSONDecodeError:
                m = re.search(r"(\[.*\])", text_out, re.DOTALL)
                if not m:
                    return []
                try:
                    data = json.loads(m.group(1))
                except json.JSONDecodeError:
                    return []

            out = []
            for it in data:
                mcq = {
                    "question": it.get("question"),
                    "options": it.get("options"),
                    "answer": it.get("answer"),
                    "source_chunk_index": idx,
                }
                if mcq["question"] and mcq["options"] and mcq["answer"]:
                    out.append(mcq)
            return out

        sem = asyncio.Semaphore(3)

        async def sem_task(i, c):
            async with sem:
                return await gen_for_chunk(i, c)

        results = await asyncio.gather(*[sem_task(i, c) for i, c in enumerate(chunks)])
        for r in results:
            questions.extend(r)

        return questions
