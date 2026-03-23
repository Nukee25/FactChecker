import asyncio
import json
import re

from services.ollama_client import generate_text

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
            evidence_urls = {
                e.get("url", "").strip()
                for e in evidence
                if isinstance(e, dict) and e.get("url")
            }

            if not evidence_urls:
                fallback = dict(FALLBACK_RESULT)
                fallback["reasoning"] = "No DuckDuckGo search evidence was found for this claim."
                fallback["evidence"] = evidence
                return fallback

            for i, e in enumerate(evidence, 1):
                evidence_lines.append(
                    f"Source {i}:\n"
                    f"  Title: {e.get('title', 'N/A')}\n"
                    f"  URL: {e.get('url', 'N/A')}\n"
                    f"  Content: {e.get('snippet', 'N/A')}"
                )
            evidence_text = "\n\n".join(evidence_lines) if evidence_lines else "No evidence available."

            prompt = f"""You are an expert fact-checker. Verify the following claim using ONLY the provided DuckDuckGo search evidence.
You MUST NOT use prior knowledge, memory, or assumptions.
If the evidence is insufficient to confirm or refute the claim, return "Unverifiable".

CLAIM: {claim}

EVIDENCE:
{evidence_text}

            Think step-by-step internally and then provide only the final JSON output.
            1. What does each source say about this claim?
            2. Is there consensus or conflict among sources?
            3. How strong is the evidence?
            4. What is your verdict?

Output ONLY a JSON object:
{{
  "verdict": "True" | "False" | "Partially True" | "Unverifiable",
  "confidence": <number 0-100>,
  "reasoning": "<clear explanation referencing specific sources>",
  "supporting_sources": [<list of source URLs from the provided evidence only>],
  "conflicting_sources": [<list of conflicting source URLs from the provided evidence only>]
}}"""

            raw = generate_text(prompt).strip()

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result["supporting_sources"] = [
                    url for url in result.get("supporting_sources", []) if url in evidence_urls
                ]
                result["conflicting_sources"] = [
                    url for url in result.get("conflicting_sources", []) if url in evidence_urls
                ]
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
