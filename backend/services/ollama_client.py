import base64
import os

import ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")
OLLAMA_VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "llava")

_client = ollama.Client(host=OLLAMA_HOST)


def generate_text(prompt: str) -> str:
    response = _client.generate(model="gemma3:4b-cloud", prompt=prompt)
    return response.response


def generate_with_image(prompt: str, image_data: bytes) -> str:
    image_b64 = base64.b64encode(image_data).decode()
    response = _client.generate(
        model="gemma3:4b-cloud",
        prompt=prompt,
        images=[image_b64],
    )
    return response.response
