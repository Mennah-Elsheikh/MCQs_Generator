import os
from flask import Flask, render_template, request
import pdfplumber
import docx
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename
import google.generativeai as genai
from fpdf import FPDF  # pip install fpdf

# Suppress PDFMiner logs
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Set Google API Key for Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyDliBF7qja0bC1b9ZgXpB4P6M7L2-seVK8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Configure Cloudinary
cloudinary.config(
    cloud_name="mcq generator",
    api_key="461395833491433",
    api_secret="vdhkkwuktdgMbrpPUK4-2yU69hg"
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        text = ' '.join([para.text for para in doc.paragraphs])
        return text
    elif ext == 'txt':
        with open(file_path, 'r') as file:
            return file.read()
    return None

def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
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
    response = model.generate_content(prompt).text.strip()
    return response

# Original local saving function
# def save_mcqs_to_file(mcqs, filename):
#     results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
#     with open(results_path, 'w') as f:
#         f.write(mcqs)
#     return results_path

# Updated to use Cloudinary
def save_mcqs_to_file(mcqs, filename):
    results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    with open(results_path, 'w') as f:
        f.write(mcqs)
    upload_result = cloudinary.uploader.upload(results_path, resource_type="raw", public_id=filename)
    return upload_result['secure_url']

# Original PDF creation (local only)
# def create_pdf(mcqs, filename):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     for mcq in mcqs.split("## MCQ"):
#         if mcq.strip():
#             pdf.multi_cell(0, 10, mcq.strip())
#             pdf.ln(5)
#     pdf_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
#     pdf.output(pdf_path)
#     return pdf_path

# Updated PDF creation with Cloudinary upload
def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)
    pdf_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    pdf.output(pdf_path)
    upload_result = cloudinary.uploader.upload(pdf_path, resource_type="raw", public_id=filename)
    return upload_result['secure_url']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_mcqs():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        text = extract_text_from_file(file_path)

        if text:
            num_questions = int(request.form['num_questions'])
            mcqs = Question_mcqs_generator(text, num_questions)

            # Original local storage and return
            # txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
            # pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
            # save_mcqs_to_file(mcqs, txt_filename)
            # create_pdf(mcqs, pdf_filename)
            # return render_template('results.html', mcqs=mcqs, txt_filename=txt_filename, pdf_filename=pdf_filename)

            # Updated Cloudinary URLs
            txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
            pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
            txt_url = save_mcqs_to_file(mcqs, txt_filename)
            pdf_url = create_pdf(mcqs, pdf_filename)

            return render_template('results.html', mcqs=mcqs, txt_url=txt_url, pdf_url=pdf_url)

    return "Invalid file format"

# Original download route (now optional)
# @app.route('/download/<filename>')
# def download_file(filename):
#     file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
#     return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    app.run(debug=True)
