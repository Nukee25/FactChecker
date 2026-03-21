import asyncio
import requests
from bs4 import BeautifulSoup

MAX_CONTENT_LINES = 200


async def extract_url_content(url: str) -> str:
    def fetch():
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            content = None
            for selector in ["article", "main", "body"]:
                element = soup.find(selector)
                if element:
                    content = element.get_text(separator="\n", strip=True)
                    break

            if not content:
                content = soup.get_text(separator="\n", strip=True)

            lines = [line.strip() for line in content.splitlines() if line.strip()]
            return "\n".join(lines[:MAX_CONTENT_LINES])
        except Exception:
            return ""

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch)
