import os

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_text(prompt: str) -> str:
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1")
    response = requests.post(
        f"{ollama_host}/api/generate",
        json={"model": ollama_model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()
