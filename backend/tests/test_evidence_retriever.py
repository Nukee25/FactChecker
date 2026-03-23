import unittest
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.evidence_retriever import retrieve_evidence


class RetrieveEvidenceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from services import evidence_retriever

        evidence_retriever._TAVILY_CLIENT = None
        evidence_retriever._TAVILY_API_KEY = None

    async def test_maps_tavily_results_to_evidence_shape(self):
        response = {
            "results": [
                {
                    "title": "Source title",
                    "url": "https://example.com/article",
                    "content": "Some matching content",
                }
            ]
        }

        with patch("services.evidence_retriever.os.getenv", return_value="test-key"), patch(
            "services.evidence_retriever.TavilyClient"
        ) as mock_client:
            mock_client.return_value.search.return_value = response
            evidence = await retrieve_evidence("A claim")

        self.assertEqual(
            evidence,
            [
                {
                    "title": "Source title",
                    "url": "https://example.com/article",
                    "snippet": "Some matching content",
                }
            ],
        )
        mock_client.return_value.search.assert_called_once_with(query="A claim", max_results=5)

    async def test_returns_empty_list_when_search_fails(self):
        with patch("services.evidence_retriever.os.getenv", return_value="test-key"), patch(
            "services.evidence_retriever.TavilyClient"
        ) as mock_client:
            mock_client.return_value.search.side_effect = RuntimeError("failure")
            evidence = await retrieve_evidence("A claim")

        self.assertEqual(evidence, [])

    async def test_returns_empty_list_when_api_key_missing(self):
        with patch("services.evidence_retriever.os.getenv", return_value=None), patch(
            "services.evidence_retriever.TavilyClient"
        ) as mock_client:
            evidence = await retrieve_evidence("A claim")

        self.assertEqual(evidence, [])
        mock_client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
