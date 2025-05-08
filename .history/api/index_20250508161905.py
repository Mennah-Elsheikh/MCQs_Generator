from flask import Flask, request, jsonify
import os
import google.generativeai as genai

# Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDliBF7qja0bC1b9ZgXpB4P6M7L2-seVK8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

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
    
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    
    try:
        response = model.generate_content(prompt).text.strip()
        return jsonify({"mcqs": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Do NOT include:
# if __name__ == "__main__":
#     app.run(debug=True)
