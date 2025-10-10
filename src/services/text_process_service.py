from typing import List
import re
from ..clients import AIClient
from ..constants import GENERATIVE_PROVIDER, CLEANER_PROMPT
from ..schemas import PagedText
from ..utils import TextHelper


class TextProcessingService:
    def __init__(self):
        self.client = AIClient.get_instance(provider=GENERATIVE_PROVIDER)

    def remove_headers(self, input_text: str) -> List[PagedText]:
        pages: List[PagedText] = []
        for page in input_text:
            repeated, page_num_patterns = TextHelper.detect_repeated_lines(page.text)
            cleaned_page_text = TextHelper.remove_headers_footers(
                page.text,
                repeated_set=repeated,
                page_num_patterns=page_num_patterns,
            )
            pages.append(PagedText(page=page.page, text=cleaned_page_text))
        return pages

    def chunk_by_token(self, pages: List[PagedText]) -> List[str]:
        """
        Chunk văn bản theo sentences, gộp lại cho đủ token.
        Simple và effective approach.
        """
        max_tokens = 500
        overlap_sentences = 2  # Số câu overlap

        # Bước 1: Gộp tất cả text từ các pages
        full_text = ""
        for page in pages:
            text = page.text.strip()
            if text:
                full_text += ("\n\n" if full_text else "") + text

        if not full_text:
            return []

        # Bước 2: Tách thành sentences
        sentences = self._split_into_sentences(full_text)
        if not sentences:
            return []

        # Bước 3: Gộp sentences thành chunks
        chunks = []
        enc = TextHelper.enc
        current_sentences = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = len(enc.encode(sentence))

            # Nếu thêm câu này vào sẽ vượt quá max_tokens
            if current_tokens + sentence_tokens > max_tokens and current_sentences:
                # Lưu chunk hiện tại
                chunk_text = " ".join(current_sentences)
                chunks.append(chunk_text)

                # Bắt đầu chunk mới với overlap
                if len(current_sentences) >= 3:
                    # Lấy 1-2 câu cuối làm overlap
                    overlap = current_sentences[-overlap_sentences:]
                    current_sentences = overlap + [sentence]
                    current_tokens = len(enc.encode(" ".join(current_sentences)))
                else:
                    # Không overlap nếu chunk trước quá ngắn
                    current_sentences = [sentence]
                    current_tokens = sentence_tokens
            else:
                # Thêm câu vào chunk hiện tại
                current_sentences.append(sentence)
                current_tokens += sentence_tokens

        # Lưu chunk cuối cùng
        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(chunk_text)

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Tách text thành sentences một cách thông minh.
        """
        # Chuẩn hóa text trước
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace
        text = text.strip()

        # Các dấu kết thúc câu
        sentence_endings = r"[.!?。！？]"

        # Tách câu nhưng giữ dấu kết thúc
        # Sử dụng lookahead để tách tại dấu câu + space + chữ hoa hoặc newline
        pattern = f"({sentence_endings}+)(?=\\s+[A-ZÀ-Ý]|\\s*$|\\n)"

        parts = re.split(pattern, text)

        sentences = []
        current = ""

        for i, part in enumerate(parts):
            if not part.strip():
                continue

            current += part

            # Nếu part là dấu kết thúc câu hoặc là phần cuối
            if re.match(sentence_endings, part) or i == len(parts) - 1:
                sentence = current.strip()
                if sentence and len(sentence) > 10:  # Bỏ qua câu quá ngắn (có thể là rác)
                    sentences.append(sentence)
                current = ""

        # Xử lý phần còn lại
        if current.strip() and len(current.strip()) > 10:
            sentences.append(current.strip())

        return sentences

    async def clean_text(self, chunk_text: str) -> str:
        prompt = CLEANER_PROMPT.format(context=chunk_text)
        resp = await self.client.chat_structured(content=[prompt], response_schema=str)
        return resp
