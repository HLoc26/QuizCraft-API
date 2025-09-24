from fastapi import APIRouter, File, UploadFile

from controllers import FilesController


# Prefix: /files
class FilesRouter:
    def __init__(self):
        self.router = APIRouter()
        self.controller = FilesController()
        self.register_routes()

    def register_routes(self):
        # POST /files/upload
        @self.router.post("/upload")
        async def create_upload_file(file: UploadFile = File(...)):
            return await self.controller.create_upload_file(file)

        # GET /files/scan/{filename}
        @self.router.get("/scan/{filename}")
        async def scan_uploaded_file(filename: str):
            return await self.controller.scan_uploaded_file(filename)

        # POST /files/scan
        @self.router.post("/scan")
        async def scan_file(file: UploadFile = File(...)):
            return await self.controller.scan_uploaded_file_direct(file)
