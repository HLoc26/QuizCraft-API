from fastapi import APIRouter
from controllers.mcq_controller import MCQController
from schemas.schema import CleanRequest, GenerateRequest, GenerateMCQRequest, ValidateMCQRequest


class MCQRouter:
    def __init__(self):
        self.router = APIRouter()
        self.controller = MCQController()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/chunk")
        async def chunk_mcq(req: GenerateRequest):
            return await self.controller.chunk(req)

        @self.router.post("/clean")
        async def clean_mcq(req: CleanRequest):
            return await self.controller.clean(req.chunks)

        @self.router.post("/generate")
        async def generate_mcq(req: GenerateMCQRequest):
            return await self.controller.generate(req.cleaned_chunks, req.question_per_chunk, req.language)

        @self.router.post("/validate")
        async def validate_mcq(req: ValidateMCQRequest):
            return await self.controller.validate(req.cleaned_chunks, req.questions)
