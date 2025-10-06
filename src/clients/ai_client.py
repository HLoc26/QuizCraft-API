from typing import List, Dict, Literal
from constants.env import GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_MODEL, OLLAMA_URL


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
        self.model = model

        if self.provider == "gemini":
            from google import genai

            self.client = genai.Client(api_key=GEMINI_API_KEY)
        elif self.provider == "local":
            from ollama import AsyncClient

            self.client = AsyncClient(OLLAMA_URL)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._initialized = True

    @staticmethod
    def get_instance(provider: Literal["local", "gemini"] = "local", model: str = None):
        if AIClient._instance is None:
            if model is None:
                if provider == "gemini":
                    model = GEMINI_MODEL
                else:
                    model = OLLAMA_MODEL
            AIClient(provider, model)
        return AIClient._instance

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        if self.provider == "local":
            resp = await self.client.chat(model=self.model, messages=messages, stream=False)
            return resp["message"]["content"]

        elif self.provider == "gemini":
            merged = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            resp = self.client.models.generate_content(model=self.model, contents=merged)

            if hasattr(resp, "text") and resp.text:
                return resp.text.strip()

            if resp.candidates:
                for c in resp.candidates:
                    if c.content and c.content.parts:
                        parts = [getattr(p, "text", "") for p in c.content.parts if getattr(p, "text", "")]
                        if parts:
                            return "".join(parts).strip()

            print("Gemini response None:", resp)
            return ""

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def chat_structured(self, content: str, response_schema):
        if self.provider != "gemini":
            raise ValueError("provider must be gemini")

        response = self.client.models.generate_content(
            model=self.model,
            contents=content,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        )

        # print(response.text)
        return response.parsed
