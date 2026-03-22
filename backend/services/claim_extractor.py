import json
import re

from services.ollama_client import generate_text
MAX_CLAIMS = 8


def extract_claims(text: str) -> list[str]:
    try:
        prompt = (
            "Extract all verifiable factual claims from the text. "
            "A verifiable claim is a specific, concrete statement that can be checked against external sources. "
            f"Extract at most {MAX_CLAIMS} claims. "
            "Output ONLY a JSON array of strings.\n\n"
            f"TEXT:\n{text}"
        )
        raw = generate_text(prompt)

        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception:
        return []
