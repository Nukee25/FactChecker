import asyncio
import os

from tavily import TavilyClient


async def retrieve_evidence(claim: str) -> list[dict]:
    def search():
        try:
            client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            response = client.search(query=claim, max_results=5)
            results = response.get("results", []) if isinstance(response, dict) else []
            evidence = []
            for r in results:
                evidence.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "snippet": r.get("content", ""),
                    }
                )
            return evidence
        except Exception:
            return []

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, search)
