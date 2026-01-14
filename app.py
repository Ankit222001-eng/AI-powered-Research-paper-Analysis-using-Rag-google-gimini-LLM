# flask_api/app.py
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# LangChain Google GenAI adapter
# NOTE: import path may vary by version — your original used langchain_google_genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing in .env")

# LLM client (LangChain adapter)
llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=API_KEY,
    temperature=0.2,
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["title", "proposal"],
    template="""
You are an expert research proposal reviewer.

TITLE:
{title}

PROPOSAL:
{proposal}

Write the following sections EXACTLY:

SUMMARY (3–5 sentences)

STRENGTHS (5 bullet points)

WEAKNESSES (5 bullet points)

SUGGESTIONS (6 numbered recommendations)

Rules:
- Section titles MUST be in ALL CAPS.
- Use professional academic tone.
- Separate each section with one blank line.
"""
)

# Runnable pipeline + parser
parser = StrOutputParser()
chain = prompt | llm | parser

app = Flask(__name__)
CORS(app)  # allow Streamlit (or other frontends) to call this API

@app.route("/health")
def health():
    return {"status": "ok", "model": MODEL}

@app.route("/analyze", methods=["POST"])
def analyze():
    payload = request.get_json(force=True, silent=True) or {}
    title = payload.get("title", "")
    proposal = payload.get("proposal", "")

    if not proposal or not proposal.strip():
        return jsonify({"error": "Proposal text required"}), 400

    try:
        # Use .invoke on Runnable pipeline
        result = chain.invoke({"title": title, "proposal": proposal})
        # result should be a string after StrOutputParser
        if not isinstance(result, str):
            # convert to JSON-safe
            result = str(result)
        return jsonify({"analysis": result})
    except Exception as e:
        # Return error with message for debugging (do not leak secrets)
        return jsonify({"error": "LLM request failed", "details": str(e)}), 500

if __name__ == "__main__":
    # Bind to 0.0.0.0 when running in container/env; for local dev 127.0.0.1 also fine
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)


#cd flask_api
#source venv/Scripts/activate

#pip install -r requirements.txt

#python app.py

#cd streamlit_app

#source venv/Scripts/activate

#pip install -r requirements.txt
#streamlit run streamlit_app.py
