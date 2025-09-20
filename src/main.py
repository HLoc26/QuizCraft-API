from fastapi import FastAPI

from utils import ResponseHelper
from routers import FilesRouter, MCQRouter


app = FastAPI()


@app.get("/")
async def get_root():
    return ResponseHelper.success({"success": True})


app.include_router(FilesRouter().router, prefix="/files", tags=["files"])
app.include_router(MCQRouter().router, prefix="/mcq", tags=["multiple_choice_question"])
