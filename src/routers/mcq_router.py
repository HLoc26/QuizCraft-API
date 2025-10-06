from fastapi import APIRouter
from controllers.mcq_controller import MCQController
from schemas.schema import GenerateRequest


class MCQRouter:
    def __init__(self):
        self.router = APIRouter()
        self.controller = MCQController()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/generate")
        async def generate_mcq(req: GenerateRequest, language):
            return await self.controller.generate(req, language)
