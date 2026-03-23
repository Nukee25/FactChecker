import unittest
from unittest.mock import patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.verifier import verify_claim


class VerifyClaimTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_unverifiable_when_no_evidence_urls(self):
        result = await verify_claim("The earth is flat", [])

        self.assertEqual(result["verdict"], "Unverifiable")
        self.assertIn("DuckDuckGo search evidence", result["reasoning"])
        self.assertEqual(result["evidence"], [])

    async def test_filters_sources_not_in_evidence(self):
        evidence = [
            {
                "title": "Trusted source",
                "url": "https://example.com/source",
                "snippet": "Snippet",
            }
        ]

        model_output = """
        {
          "verdict": "True",
          "confidence": 88,
          "reasoning": "Supported by source.",
          "supporting_sources": ["https://example.com/source", "https://not-in-evidence.com"],
          "conflicting_sources": ["https://other-unknown.com"]
        }
        """

        with patch("services.verifier.generate_text", return_value=model_output):
            result = await verify_claim("A test claim", evidence)

        self.assertEqual(result["verdict"], "True")
        self.assertEqual(result["supporting_sources"], ["https://example.com/source"])
        self.assertEqual(result["conflicting_sources"], [])
        self.assertEqual(result["evidence"], evidence)


if __name__ == "__main__":
    unittest.main()
