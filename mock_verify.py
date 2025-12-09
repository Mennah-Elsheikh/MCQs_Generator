import sys
import os
from unittest.mock import MagicMock

# Mock everything missing
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["cloudinary"] = MagicMock()
sys.modules["cloudinary.uploader"] = MagicMock()
sys.modules["fpdf"] = MagicMock()

# Mock Config if needed, but it relies on dotenv which IS installed
# If dotenv is not installed, we should mock it too? 
# I previously installed python-dotenv successfully.

# Add current directory to path
sys.path.append(os.getcwd())

from src.services.mcq_service import generate_mcqs_from_text
from src.services.storage_service import save_mcqs_to_file, create_pdf

def test_mocked_execution():
    print("Testing with Mocks...")
    
    # Setup Mocks
    genai_mock = sys.modules["google.generativeai"]
    model_mock = MagicMock()
    genai_mock.GenerativeModel.return_value = model_mock
    model_mock.generate_content.return_value.text = "## MCQ\nQuestion: Mock?\nA) Yes\nB) No\nCorrect Answer: A"

    cloudinary_mock = sys.modules["cloudinary.uploader"]
    cloudinary_mock.upload.return_value = {'secure_url': 'http://mock.url/file.pdf'}

    # Test Generation
    print("1. Testing Generation logic...")
    # The module imports happen at top level, so the real classes are replaced by mocks effectively if we did it right
    # However, inside mcq_service.py, it does `model = genai.GenerativeModel(...)` at import time.
    # Since we mocked sys.modules BEFORE import, it should use the mock.
    
    # We need to reload the module if it was already imported, but this script is fresh.
    
    try:
        mcqs = generate_mcqs_from_text("Test text", 1)
        print(f"Generated: {mcqs}")
    except Exception as e:
        print(f"Generation failed: {e}")

    # Test Storage
    print("2. Testing Storage logic...")
    try:
        url = save_mcqs_to_file("Content", "test.txt")
        print(f"Saved Text URL: {url}")
        
        pdf_url = create_pdf("Content", "test.pdf")
        print(f"Saved PDF URL: {pdf_url}")
    except Exception as e:
        print(f"Storage failed: {e}")

if __name__ == "__main__":
    test_mocked_execution()
