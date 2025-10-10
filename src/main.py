from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .clients import AIClient
from utils import ResponseHelper
from routers import FilesRouter, MCQRouter


app = FastAPI()


@app.get("/")
async def get_root():
    return ResponseHelper.success({"success": True})


@app.get("/hello/gemini")
async def hello():
    return await AIClient("gemini").chat(messages=[{"role": "system", "content": "Your task is to response hello whenever receive a message"}, {"role": "user", "content": "hello"}])


origins = ["http://localhost:5173"]
methods = ["GET", "POST", "DELETE"]
headers = ["Content-Type", "Authorization"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)
app.include_router(FilesRouter().router, prefix="/files", tags=["files"])
app.include_router(MCQRouter().router, prefix="/mcq", tags=["multiple_choice_question"])
