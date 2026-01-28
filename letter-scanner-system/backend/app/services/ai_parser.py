import os
import google.generativeai as genai
import json

# Read API key from Railway environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def extract_letter_fields(text: str) -> dict:
    """
    Uses Gemini AI (free tier) to extract structured data from letter text.
    Returns guaranteed JSON.
    """

    prompt = f"""
You are an expert office clerk.

From the letter text below, extract the following fields:
- from
- to
- date
- subject

Rules:
- If a field is missing, return empty string ""
- Date must be in YYYY-MM-DD format if possible
- Return ONLY valid JSON
- Do not add explanations

Letter Text:
\"\"\"
{text}
\"\"\"

JSON format:
{{
  "from": "",
  "to": "",
  "date": "",
  "subject": ""
}}
"""

    response = model.generate_content(prompt)

    # Safety: ensure JSON even if Gemini adds text
    try:
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        clean_json = response.text[json_start:json_end]
        return json.loads(clean_json)
    except Exception:
        return {
            "from": "",
            "to": "",
            "date": "",
            "subject": ""
        }
