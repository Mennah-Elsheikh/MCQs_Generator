import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from src.config import Config
from src.services.mcq_service import generate_mcqs_from_text
from src.services.storage_service import save_mcqs_to_file

def test_config():
    print("Testing Config...")
    try:
        Config.validate()
        print("Config validation passed.")
    except Exception as e:
        print(f"Config validation failed: {e}")

def test_mcq_generation():
    print("Testing MCQ Generation...")
    text = "Artificial Intelligence is the simulation of human intelligence processes by machines."
    try:
        mcqs = generate_mcqs_from_text(text, 1)
        print("MCQ Generation successful.")
        return mcqs
    except Exception as e:
        print(f"MCQ Generation failed: {e}")
        return None

def test_storage(mcqs):
    print("Testing Storage...")
    if mcqs:
        try:
            url = save_mcqs_to_file(mcqs, "test_mcq.txt")
            print(f"Storage successful. URL/Path: {url}")
        except Exception as e:
            print(f"Storage failed: {e}")

if __name__ == "__main__":
    test_config()
    mcqs = test_mcq_generation()
    test_storage(mcqs)
