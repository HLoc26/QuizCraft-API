from fastapi import APIRouter
from controllers.mcq_controller import MCQController
from schemas.request import GenerateRequest, GenerateResponse


class MCQRouter:
    def __init__(self):
        self.router = APIRouter()
        self.controller = MCQController()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/generate", response_model=GenerateResponse)
        async def generate_mcq(req: GenerateRequest):
            return await self.controller.generate(req)
