import asyncio
import json
import re

from services.ollama_client import generate_text

FALLBACK_RESULT = {
    "ai_probability": 50,
    "human_probability": 50,
    "confidence": 0,
    "indicators": ["Analysis unavailable"],
}


async def detect_ai_content(text: str) -> dict:
    def analyze():
        try:
            prompt = f"""Analyze the following text and determine the likelihood that it was written by an AI vs a human.

TEXT:
{text[:3000]}

Evaluate writing style, vocabulary patterns, sentence structure, repetition, and other indicators.

Output ONLY a JSON object:
{{
  "ai_probability": <number 0-100>,
  "human_probability": <number 0-100>,
  "confidence": <number 0-100>,
  "indicators": ["<indicator 1>", "<indicator 2>", ...]
}}

Ensure ai_probability + human_probability = 100."""

            raw = generate_text(prompt).strip()
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            return dict(FALLBACK_RESULT)
        except Exception:
            return dict(FALLBACK_RESULT)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, analyze)
