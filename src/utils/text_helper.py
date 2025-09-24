import re
from typing import List


class TextHelper:
    @staticmethod
    def clean_text(t: str) -> str:
        """Chuẩn hoá text: bỏ khoảng trắng thừa, xử lý dấu câu cơ bản"""
        t = re.sub(r"\s+", " ", t).strip()
        t = re.sub(r"[.]{3,}", "…", t)  # thay ... bằng …
        return t

    @staticmethod
    def chunk_text_by_word(text: str, max_words: int = 400, overlap_words: int = 50) -> List[str]:
        """
        Chia text thành các chunk:
        - Ngắt theo câu trước (ưu tiên giữ nguyên câu)
        - Giới hạn số từ trong mỗi chunk
        - Thêm overlap (ngữ cảnh chồng lấn) giữa các chunk
        """
        if not text.strip():
            return []

        # Tách câu cho tiếng Việt (hỗ trợ ., ?, !, …)
        sentences = re.split(r"(?<=[.!?…])\s+", text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks: List[str] = []
        current_words: List[str] = []

        for sentence in sentences:
            sentence_words = sentence.split()

            # Nếu 1 câu quá dài → cắt nhỏ theo từ
            while len(sentence_words) > max_words:
                chunks.append(" ".join(sentence_words[:max_words]))
                sentence_words = sentence_words[max_words:]

            # Nếu thêm câu này vào chunk sẽ vượt max_words
            if len(current_words) + len(sentence_words) > max_words and current_words:
                chunks.append(" ".join(current_words))

                # Lấy overlap
                overlap = current_words[-overlap_words:] if overlap_words > 0 else []
                current_words = overlap + sentence_words
            else:
                current_words.extend(sentence_words)

        # Add chunk cuối
        if current_words:
            chunks.append(" ".join(current_words))

        return chunks

    @staticmethod
    def chunk_text_by_paragraph(text: str, max_words: int = 400) -> List[str]:
        """Chia theo đoạn văn, sau đó fallback sang chunk theo câu nếu đoạn quá dài"""
        paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks: List[str] = []
        current_words: List[str] = []

        for paragraph in paragraphs:
            para_words = paragraph.split()

            if len(para_words) > max_words:
                # Lưu chunk hiện tại rồi chia đoạn lớn theo câu
                if current_words:
                    chunks.append(" ".join(current_words))
                    current_words = []
                chunks.extend(TextHelper.chunk_text_by_word(paragraph, max_words))
            elif len(current_words) + len(para_words) > max_words and current_words:
                chunks.append(" ".join(current_words))
                current_words = para_words
            else:
                current_words.extend(para_words)

        if current_words:
            chunks.append(" ".join(current_words))

        return chunks

    @staticmethod
    def get_text_stats(text: str) -> dict:
        """Thống kê cơ bản về text"""
        sentences = re.split(r"(?<=[.!?…])\s+", text.strip())
        sentences = [s for s in sentences if s.strip()]

        words = text.split()
        paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        return {
            "total_words": len(words),
            "total_sentences": len(sentences),
            "total_paragraphs": len(paragraphs),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "avg_sentences_per_paragraph": len(sentences) / len(paragraphs) if paragraphs else 0,
        }
