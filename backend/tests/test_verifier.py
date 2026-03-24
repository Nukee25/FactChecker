import unittest
from unittest.mock import AsyncMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.verifier import verify_claim


class VerifyClaimTests(unittest.IsolatedAsyncioTestCase):
    async def test_retrieves_ddgs_evidence_when_none_provided(self):
        ddgs_evidence = [
            {
                "title": "Trusted source",
                "url": "https://example.com/source",
                "snippet": "Snippet",
            }
        ]
        model_output = """
        {
          "verdict": "True",
          "confidence": 90,
          "reasoning": "Supported by source.",
          "supporting_sources": ["https://example.com/source"],
          "conflicting_sources": []
        }
        """

        with patch("services.verifier.retrieve_evidence", new=AsyncMock(return_value=ddgs_evidence)) as mock_retrieve:
            with patch("services.verifier.generate_text", return_value=model_output):
                result = await verify_claim("A test claim", [])

        mock_retrieve.assert_awaited_once_with("A test claim")
        self.assertEqual(result["verdict"], "True")
        self.assertEqual(result["supporting_sources"], ["https://example.com/source"])
        self.assertEqual(result["evidence"], ddgs_evidence)

    async def test_returns_unverifiable_when_no_evidence_urls(self):
        with patch("services.verifier.retrieve_evidence", new=AsyncMock(return_value=[])):
            result = await verify_claim("The earth is flat", [])

        self.assertEqual(result["verdict"], "Unverifiable")
        self.assertIn("DuckDuckGo search evidence URLs", result["reasoning"])
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
