import os
import cloudinary
import cloudinary.uploader
from fpdf import FPDF
from src.config import Config

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

def save_mcqs_to_file(mcqs, filename):
    results_path = os.path.join(Config.RESULTS_FOLDER, filename)
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write(mcqs)
    
    # Upload to Cloudinary if configured
    if Config.CLOUDINARY_CLOUD_NAME:
        try:
            upload_result = cloudinary.uploader.upload(results_path, resource_type="raw", public_id=filename)
            return upload_result['secure_url']
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            return None
    return results_path # Return local path if upload not configured/failed

def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            # Handle unicode issues in FPDF roughly by encoding/decoding or using specific fonts if needed
            # For now, sticking to basic latin-1 compat or ignoring errors
            clean_text = mcq.strip().encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, clean_text)
            pdf.ln(5)
    
    pdf_path = os.path.join(Config.RESULTS_FOLDER, filename)
    pdf.output(pdf_path)

    # Upload to Cloudinary if configured
    if Config.CLOUDINARY_CLOUD_NAME:
        try:
            upload_result = cloudinary.uploader.upload(pdf_path, resource_type="raw", public_id=filename)
            return upload_result['secure_url']
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            return None
    return pdf_path
