import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.config import Config
from src.utils.file_utils import allowed_file, extract_text_from_file
from src.services.mcq_service import generate_mcqs_from_text
from src.services.storage_service import save_mcqs_to_file, create_pdf

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_mcqs():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        text = extract_text_from_file(file_path)

        if text:
            try:
                num_questions = int(request.form['num_questions'])
                mcqs = generate_mcqs_from_text(text, num_questions)

                txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
                pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
                
                txt_url = save_mcqs_to_file(mcqs, txt_filename)
                pdf_url = create_pdf(mcqs, pdf_filename)

                return render_template('results.html', mcqs=mcqs, txt_url=txt_url, pdf_url=pdf_url)
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

    return "Invalid file format", 400

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    app.run(debug=True)

