import numpy as np
import pytesseract
from PIL import Image
import easyocr


class OCRService:
    def __init__(self):
        self.easyocr_reader = easyocr.Reader(["en", "vi"])

    async def use_tesseract(self, file_path: str):
        return pytesseract.image_to_string(Image.open(file_path))

    async def use_easyocr(self, image: Image.Image | str):
        if isinstance(image, str):
            result = self.easyocr_reader.readtext(image, detail=0)
        else:
            result = self.easyocr_reader.readtext(np.array(image), detail=0)
        return "\n".join(result)
