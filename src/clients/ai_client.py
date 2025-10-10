import json
import re
from typing import List, Dict, Literal, Any
from ..constants import GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_MODEL, OLLAMA_URL


class AIClient:
    _instance = None

    def __new__(cls, provider: Literal["local", "gemini"] = "local", model: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, provider: Literal["local", "gemini"] = "local", model: str = None):
        if getattr(self, "_initialized", False):
            return

        self.provider = provider
        self.model = model or (GEMINI_MODEL if provider == "gemini" else OLLAMA_MODEL)

        if self.provider == "gemini":
            from google import genai

            self.client = genai.Client(api_key=GEMINI_API_KEY)

        elif self.provider == "local":
            from ollama import AsyncClient

            self.client = AsyncClient(host=OLLAMA_URL)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._initialized = True

    @staticmethod
    def get_instance(provider: Literal["local", "gemini"] = "local", model: str = None):
        if AIClient._instance is None:
            AIClient(provider, model)
        return AIClient._instance

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """Unstructured text chat"""
        if self.provider == "local":
            resp = await self.client.chat(model=self.model, messages=messages, stream=False)
            return resp["message"]["content"]

        elif self.provider == "gemini":
            merged = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            resp = self.client.models.generate_content(model=self.model, contents=merged)
            text = getattr(resp, "text", None)
            if text:
                return text.strip()

            if getattr(resp, "candidates", None):
                for c in resp.candidates:
                    if c.content and c.content.parts:
                        parts = [getattr(p, "text", "") for p in c.content.parts if getattr(p, "text", "")]
                        if parts:
                            return "".join(parts).strip()
            return ""

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def chat_structured(self, content: str, response_schema: Any):
        """Structured response (JSON-like)"""
        if self.provider == "gemini":
            response = self.client.models.generate_content(
                model=self.model,
                contents=content,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": response_schema,
                },
            )
            return response.parsed

        elif self.provider == "local":
            # Giả lập structured output bằng cách yêu cầu model trả JSON
            messages = [
                {"role": "user", "content": content},
            ]
            resp = await self.chat(messages)
            try:
                # Loại bỏ markdown fence (``` hoặc ```json)
                cleaned = re.sub(r"```(?:json)?|```", "", resp).strip()
                # Bỏ dấu phẩy thừa trước dấu đóng mảng hoặc object
                cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
                # Giữ lại phần JSON chính (từ [ ... ] hoặc { ... })
                match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
                if not match:
                    raise ValueError("No valid JSON structure found in response")
                json_str = match.group(1)
                return json.loads(json_str)
            except Exception as e:
                print("[chat_structured][local] JSON parse failed with error", e)
                print("[chat_structured][local] raw response:")
                print(resp)
                return None

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
