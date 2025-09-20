import io
import os
import docx
import pymupdf
from constants import UPLOAD_FOLDER
from .ocr_service import OCRService
from PIL import Image


class ScanService:
    def __init__(self):
        self.UPLOAD_FOLDER: str = UPLOAD_FOLDER
        self.ocr_service = OCRService()

    def get_path(self, filename):
        return os.path.join(self.UPLOAD_FOLDER, filename)

    async def scan_pdf(self, filename: str):
        file_path: str = self.get_path(filename)
        text: str = ""
        doc = pymupdf.open(file_path)

        for page in doc:
            extracted = page.get_textbox("")
            if extracted.strip():
                text += extracted + "\n"
            else:
                print("Using OCR due to extracted is", extracted)
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text = await self.ocr_service.use_easyocr(img)
                text += ocr_text + "\n"
        return text

    async def scan_image(self, filename: str):
        file_path: str = self.get_path(filename)
        text: str = ""
        text = await self.ocr_service.use_easyocr(file_path)
        return text

    async def scan_text(self, filename: str):
        file_path: str = self.get_path(filename)
        text: str = ""
        with open(file_path, "r", encoding="utf-8") as f:
            text += f.read()
        return text

    async def scan_docx(self, filename: str):
        file_path: str = self.get_path(filename)
        text: str = ""
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
