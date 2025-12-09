import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    UPLOAD_FOLDER = 'uploads/'
    RESULTS_FOLDER = 'results/'
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}

    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            raise RuntimeError("GOOGLE_API_KEY is not set. Add it to your environment or .env file.")
