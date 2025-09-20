import os
from fastapi import File, UploadFile

from constants import UPLOAD_FOLDER
from services import ScanService, UploadService
from utils import ResponseHelper


class FilesController:
    def __init__(self):
        self.scan_service: ScanService = ScanService()
        self.upload_service: UploadService = UploadService()
        self.UPLOAD_FOLDER: str = UPLOAD_FOLDER
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

    async def create_upload_file(self, file: UploadFile = File(...)):
        try:
            filename = await self.upload_service.upload_file(file)

            if filename:
                return ResponseHelper.success({"filename": filename, "message": "File uploaded successfully!"})
            else:
                raise Exception("Error while uploading file that cause filename to be Null")
        except Exception as e:
            return ResponseHelper.error(e.__str__())

    async def scan_file(self, filename: str):
        text = ""
        try:
            if filename.lower().endswith(".pdf"):
                text = await self.scan_service.scan_pdf(filename)

            elif filename.lower().endswith((".png", ".jpeg", ".jpg")):
                text = await self.scan_service.scan_image(filename)

            elif filename.lower().endswith((".txt", ".md")):
                text = await self.scan_service.scan_text(filename)

            elif filename.lower().endswith(".docx"):
                text = await self.scan_service.scan_docx(filename)

            else:
                return ResponseHelper.error("Unsupported file type.")

            return ResponseHelper.success({"filename": filename, "text": text})
        except ValueError as e:
            return ResponseHelper.error(e.__str__())
