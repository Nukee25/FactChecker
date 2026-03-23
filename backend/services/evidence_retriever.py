import asyncio
import os

from tavily import TavilyClient

_TAVILY_CLIENT = None
_TAVILY_API_KEY = None


async def retrieve_evidence(claim: str) -> list[dict]:
    def search():
        global _TAVILY_CLIENT, _TAVILY_API_KEY
        try:
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                return []

            if _TAVILY_CLIENT is None or _TAVILY_API_KEY != api_key:
                _TAVILY_CLIENT = TavilyClient(api_key=api_key)
                _TAVILY_API_KEY = api_key

            response = _TAVILY_CLIENT.search(query=claim, max_results=5)
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
