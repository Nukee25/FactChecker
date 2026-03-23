import asyncio
import json
import re

import requests

from services.ollama_client import generate_with_image

FALLBACK_RESULT = {
    "is_authentic": None,
    "manipulation_probability": 50,
    "ai_generated_probability": 50,
    "confidence": 0,
    "indicators": ["Analysis unavailable"],
    "summary": "Could not analyze media",
}

MEDIA_PROMPT = """Analyze this image carefully for signs of manipulation, deepfake, or AI generation.

Evaluate the following aspects:
1. Visual artifacts, blurring, or inconsistencies at object boundaries
2. Unnatural textures, repeated patterns, or overly smooth surfaces
3. Lighting and shadow inconsistencies across the scene
4. Signs of digital compositing (cloning, copy-paste, splicing)
5. Facial anomalies (if people are present): unnatural eyes, teeth, ears, or hair
6. GAN/diffusion model artifacts (e.g., uniform skin texture, background noise)

Output ONLY a JSON object:
{
  "is_authentic": <true if the image appears authentic, false if likely manipulated or AI-generated>,
  "manipulation_probability": <number 0-100, probability of manual manipulation>,
  "ai_generated_probability": <number 0-100, probability of being AI-generated>,
  "confidence": <number 0-100, your confidence in this assessment>,
  "indicators": ["<specific indicator 1>", "<specific indicator 2>", ...],
  "summary": "<brief plain-language summary of findings>"
}"""


async def check_media_authenticity(image_data: bytes) -> dict:
    def analyze():
        try:
            raw = generate_with_image(MEDIA_PROMPT, image_data).strip()
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            return dict(FALLBACK_RESULT)
        except Exception:
            return dict(FALLBACK_RESULT)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, analyze)


async def check_media_from_url(url: str) -> dict:
    def fetch():
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.content

    loop = asyncio.get_event_loop()
    image_data = await loop.run_in_executor(None, fetch)
    return await check_media_authenticity(image_data)
