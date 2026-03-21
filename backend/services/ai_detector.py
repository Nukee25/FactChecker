import asyncio
import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_FALLBACK = {
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

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            raw = response.text.strip()

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())

            return dict(_FALLBACK)
        except Exception:
            return dict(_FALLBACK)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, analyze)
