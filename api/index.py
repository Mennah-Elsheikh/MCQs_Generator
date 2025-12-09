from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to path to allow imports from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.mcq_service import generate_mcqs_from_text
from src.config import Config

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "MCQs Generator API is running!"

@app.route('/api/generate', methods=['POST'])
def generate_mcqs():
    data = request.json
    if not data or 'text' not in data or 'num_questions' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    text = data['text']
    num_questions = data['num_questions']
    
    try:
        # Re-initialize config inside the function if needed for serverless environments
        # or rely on the import time configuration
        Config.validate()
        response = generate_mcqs_from_text(text, num_questions)
        return jsonify({"mcqs": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

