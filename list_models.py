import google.generativeai as genai
from src.config import Config
import os

# Ensure API key is set
Config.validate()
genai.configure(api_key=Config.GOOGLE_API_KEY)

print(f"Using API Key: {Config.GOOGLE_API_KEY[:5]}... (masked)")

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
