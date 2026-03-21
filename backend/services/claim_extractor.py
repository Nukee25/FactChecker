import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MAX_CLAIMS = 8


def extract_claims(text: str) -> list[str]:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Extract all verifiable factual claims from the text. "
            "A verifiable claim is a specific, concrete statement that can be checked against external sources. "
            f"Extract at most {MAX_CLAIMS} claims. "
            "Output ONLY a JSON array of strings.\n\n"
            f"TEXT:\n{text}"
        )
        response = model.generate_content(prompt)
        raw = response.text.strip()

        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception:
        return []
