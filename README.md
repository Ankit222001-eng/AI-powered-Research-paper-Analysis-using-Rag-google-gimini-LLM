# Gemini 1.5 — Flask API + Streamlit UI

This repository contains a ready-to-run project that:

- Implements a Flask API that talks to Google's Gemini (Gemini 1.5) model using the `google-genai` Python SDK.
- Implements a Streamlit frontend that calls the Flask API to perform research-proposal analysis (summarize, strengths, weaknesses, suggestions) using the LLM.
- Supports uploading PDF and image files; extracts text using pdfplumber (PDF) or pytesseract (image OCR).

## Quick start (local)

### 1) Set up the Flask API
```bash
cd flask_api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# edit .env to set GOOGLE_API_KEY and model name
python app.py
```

### 2) Set up the Streamlit UI
```bash
cd ../streamlit_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Point the `FLASK_API_BASE` env var to your running Flask API (or deploy Flask and set to the hosted URL).

## Notes
- You will need Tesseract OCR installed on the system (for pytesseract to work) if you want image OCR. See Tesseract installation instructions for your OS.
- The Google `google-genai` SDK package name and usage may change. If `genai.Client(...).generate_text(...)` fails, follow Google’s official quickstart docs and adapt the client call accordingly.
- Model name used in `.env.example` is an example. You may need to change it depending on access.
