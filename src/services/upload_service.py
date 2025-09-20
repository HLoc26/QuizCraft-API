import os
from fastapi import File, UploadFile


class UploadService:
    def __init__(self):
        self.UPLOAD_FOLDER = "uploads"

    def get_unique_name(self, filename: str):
        name, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(os.path.join(self.UPLOAD_FOLDER, new_filename)):
            new_filename = f"{name}({counter}){ext}"
            counter += 1

        return new_filename

    async def upload_file(self, file: UploadFile = File(...)):
        unique_name = self.get_unique_name(file.filename)
        file_path = os.path.join(self.UPLOAD_FOLDER, unique_name)

        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
        except Exception as e:
            raise e

        return unique_name
