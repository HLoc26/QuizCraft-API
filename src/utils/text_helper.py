from collections import Counter
import json
import re
from typing import List

import tiktoken


class TextHelper:
    enc = tiktoken.get_encoding("cl100k_base")

    @staticmethod
    def clean_text(t: str) -> str:
        """Chuẩn hoá text: bỏ khoảng trắng thừa, xử lý dấu câu cơ bản"""
        t = re.sub(r"\s+", " ", t).strip()
        t = re.sub(r"[.]{3,}", "…", t)  # thay ... bằng …
        return t

    @staticmethod
    def detect_repeated_lines(pages_texts, min_frac=0.4):
        # pages_texts: list of page["text"]
        per_page_lines = []
        for t in pages_texts:
            lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
            per_page_lines.append(lines)
        counts = Counter()
        for lines in per_page_lines:
            unique = set(lines)
            counts.update(unique)
        n_pages = len(per_page_lines)
        repeated = {ln for ln, c in counts.items() if c / n_pages >= min_frac}
        # also add common page-number patterns
        import re

        page_num_patterns = [re.compile(r"^\s*page\s*\d+\b", re.IGNORECASE), re.compile(r"^\s*\d+\s*\/\s*\d+\s*$"), re.compile(r"^\s*\d+\s*$")]
        return repeated, page_num_patterns

    @staticmethod
    def remove_headers_footers(page_text: str, repeated_set, page_num_patterns):
        out_lines = []
        for ln in page_text.splitlines():
            s = ln.strip()
            if not s:
                continue
            if s in repeated_set:
                continue
            if any(p.match(s) for p in page_num_patterns):
                continue
            out_lines.append(ln)
        return "\n".join(out_lines)

    @staticmethod
    def chunk_text_with_tokens(text, max_tokens=500, overlap=50) -> List[str]:
        toks = TextHelper.enc.encode(text)
        chunks = []
        i = 0
        idx = 0
        while i < len(toks):
            chunk_toks = toks[i : i + max_tokens]
            chunk_text = TextHelper.enc.decode(chunk_toks)
            chunks.append({"chunk_index": idx, "start_token": i, "text": chunk_text})
            idx += 1
            i += max_tokens - overlap
        return chunks

    @staticmethod
    def extract_json(resp: str):
        # Tìm đoạn JSON nằm trong code block nếu có
        match = re.search(r"```(?:json)?\s*(\[\{.*\}\])\s*```", resp, re.DOTALL)
        if match:
            return json.loads(match.group(1))

        # Nếu không có code block → thử parse trực tiếp
        return json.loads(resp)
