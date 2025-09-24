from fastapi import UploadFile, File
from utils import ResponseHelper
from constants import UPLOAD_FOLDER
from services import ScanService, UploadService
import os


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
            return ResponseHelper.error(str(e))

    # 1. Scan từ file đã tồn tại trong UPLOAD_FOLDER (tham số là string)
    async def scan_uploaded_file(self, filename: str):
        try:
            lower_name = filename.lower()

            if lower_name.endswith(".pdf"):
                text = await self.scan_service.scan_pdf(filename)

            elif lower_name.endswith((".png", ".jpeg", ".jpg")):
                text = await self.scan_service.scan_image(filename)

            elif lower_name.endswith((".txt", ".md")):
                text = await self.scan_service.scan_text(filename)

            elif lower_name.endswith(".docx"):
                text = await self.scan_service.scan_docx(filename)

            else:
                return ResponseHelper.error("Unsupported file type.")

            return ResponseHelper.success({"filename": filename, "text": text})
        except Exception as e:
            return ResponseHelper.error(str(e))

    # 2. Scan trực tiếp từ file upload (UploadFile)
    async def scan_uploaded_file_direct(self, file: UploadFile = File(...)):
        try:
            filename = file.filename.lower()

            if filename.endswith(".pdf"):
                text = await self.scan_service.scan_pdf(file.file)

            elif filename.endswith((".png", ".jpeg", ".jpg")):
                text = await self.scan_service.scan_image(file.file)

            elif filename.endswith((".txt", ".md")):
                text = await self.scan_service.scan_text(file.file)

            elif filename.endswith(".docx"):
                text = await self.scan_service.scan_docx(file.file)

            else:
                return ResponseHelper.error("Unsupported file type.")

            return ResponseHelper.success({"filename": file.filename, "text": text})
        except Exception as e:
            return ResponseHelper.error(str(e))
