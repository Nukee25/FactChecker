import asyncio

from duckduckgo_search import DDGS


async def retrieve_evidence(claim: str) -> list[dict]:
    def search():
        try:
            with DDGS() as ddgs:
                results = ddgs.text(claim, max_results=5)
                evidence = []
                for r in results:
                    evidence.append(
                        {
                            "title": r.get("title", ""),
                            "url": r.get("href", ""),
                            "snippet": r.get("body", ""),
                        }
                    )
                return evidence
        except Exception:
            return []

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, search)
