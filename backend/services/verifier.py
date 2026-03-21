import asyncio
import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

FALLBACK_RESULT = {
    "verdict": "Unverifiable",
    "confidence": 0,
    "reasoning": "Could not analyze",
    "supporting_sources": [],
    "conflicting_sources": [],
}


async def verify_claim(claim: str, evidence: list) -> dict:
    def analyze():
        try:
            evidence_lines = []
            for i, e in enumerate(evidence, 1):
                evidence_lines.append(
                    f"Source {i}:\n"
                    f"  Title: {e.get('title', 'N/A')}\n"
                    f"  URL: {e.get('url', 'N/A')}\n"
                    f"  Content: {e.get('snippet', 'N/A')}"
                )
            evidence_text = "\n\n".join(evidence_lines) if evidence_lines else "No evidence available."

            prompt = f"""You are an expert fact-checker. Verify the following claim using ONLY the provided evidence.

CLAIM: {claim}

EVIDENCE:
{evidence_text}

Using Chain of Thought reasoning:
1. What does each source say about this claim?
2. Is there consensus or conflict among sources?
3. How strong is the evidence?
4. What is your verdict?

Output ONLY a JSON object:
{{
  "verdict": "True" | "False" | "Partially True" | "Unverifiable",
  "confidence": <number 0-100>,
  "reasoning": "<clear explanation referencing specific sources>",
  "supporting_sources": [<list of source URLs>],
  "conflicting_sources": [<list of conflicting source URLs if any>]
}}"""

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            raw = response.text.strip()

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result["evidence"] = evidence
                return result

            fallback = dict(FALLBACK_RESULT)
            fallback["evidence"] = evidence
            return fallback
        except Exception:
            fallback = dict(FALLBACK_RESULT)
            fallback["evidence"] = evidence
            return fallback

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, analyze)
