# MCQs Generator

A Flask web application that generates multiple-choice questions (MCQs) from uploaded documents using Google's Generative AI (Gemini).

## Features

- **File Upload Support**: Extract text from PDF, DOCX, and TXT files
- **AI-Powered MCQ Generation**: Uses Gemini AI to create contextual multiple-choice questions
- **Export Options**: Download generated MCQs as TXT or PDF
- **Cloud Storage**: Optional Cloudinary integration for file storage
- **Clean Architecture**: Modular codebase with separation of concerns

## Project Structure

```
MCQs_Generator/
├── app.py                  # Flask application entry point
├── api/
│   └── index.py           # Vercel serverless API endpoint
├── src/
│   ├── config.py          # Configuration and environment variables
│   ├── services/
│   │   ├── mcq_service.py     # Gemini AI integration
│   │   └── storage_service.py # File storage & PDF generation
│   └── utils/
│       └── file_utils.py      # File parsing utilities
├── templates/             # HTML templates
├── uploads/              # Temporary file uploads
└── results/              # Generated MCQ files
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
GOOGLE_API_KEY=your_google_api_key_here
CLOUDINARY_CLOUD_NAME=your_cloud_name_here  # Optional
CLOUDINARY_API_KEY=your_cloudinary_api_key_here  # Optional
CLOUDINARY_API_SECRET=your_cloudinary_api_secret_here  # Optional
```

**Get your Google API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate a free API key.

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Usage

1. Open the application in your browser
2. Upload a PDF, DOCX, or TXT file
3. Specify the number of MCQs to generate
4. Click "Generate MCQs"
5. Download the results as TXT or PDF

## Technologies

- **Backend**: Flask, Python 3.10+
- **AI**: Google Generative AI (Gemini)
- **File Processing**: pdfplumber, python-docx
- **PDF Generation**: FPDF
- **Cloud Storage**: Cloudinary (optional)

## License

MIT License