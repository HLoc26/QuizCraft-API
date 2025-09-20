import re
from typing import List


class TextHelper:
    @staticmethod
    def clean_text(t: str) -> str:
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @staticmethod
    def chunk_text_by_word(text: str, max_words: int = 400):
        words = text.split()
        chunks: List[str] = []

        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i : i + max_words])
            chunks.append(chunk)
        return chunks
