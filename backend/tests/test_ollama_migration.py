import asyncio
import unittest
from unittest.mock import patch

from services.ai_detector import FALLBACK_RESULT
from services.ai_detector import detect_ai_content
from services.claim_extractor import extract_claims
from services.ollama_client import generate_text
from services.verifier import verify_claim


class OllamaMigrationTests(unittest.TestCase):
    def test_extract_claims_parses_json_array_from_model_output(self):
        with patch("services.claim_extractor.generate_text", return_value='["A", "B"]'):
            self.assertEqual(extract_claims("text"), ["A", "B"])

    def test_detect_ai_content_returns_fallback_on_invalid_model_output(self):
        with patch("services.ai_detector.generate_text", return_value="not-json"):
            result = asyncio.run(detect_ai_content("text"))
        self.assertEqual(result, FALLBACK_RESULT)

    def test_verify_claim_appends_evidence_on_success(self):
        evidence = [{"title": "t", "url": "https://example.com", "snippet": "s"}]
        model_output = (
            '{"verdict":"True","confidence":90,"reasoning":"supported",'
            '"supporting_sources":["https://example.com"],"conflicting_sources":[]}'
        )
        with patch("services.verifier.generate_text", return_value=model_output):
            result = asyncio.run(verify_claim("claim", evidence))
        self.assertEqual(result["verdict"], "True")
        self.assertEqual(result["evidence"], evidence)

    def test_ollama_client_calls_local_generate_endpoint(self):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {"response": "hello"}
        mock_response.raise_for_status.return_value = None
        with patch("services.ollama_client.requests.post", return_value=mock_response) as mock_post:
            result = generate_text("prompt text")
        self.assertEqual(result, "hello")
        call_url = mock_post.call_args.args[0]
        call_json = mock_post.call_args.kwargs["json"]
        self.assertTrue(call_url.endswith("/api/generate"))
        self.assertEqual(call_json["prompt"], "prompt text")
        self.assertFalse(call_json["stream"])


if __name__ == "__main__":
    unittest.main()
