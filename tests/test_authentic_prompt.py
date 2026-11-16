"""Regression tests for condition masking in the authentic API experiment.

Network calls are mocked: running these tests makes no paid API requests.
"""
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from culturaeval.authentic_pilot import CONDITIONS, request


class TestAuthenticPromptMasking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path("data/authentic_pilot_candidates.jsonl")
        cls.cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_all_conditions_masked_for_both_cases(self):
        for case in self.cases:
            for condition in CONDITIONS:
                with self.subTest(case=case["id"], condition=condition):
                    captured = []

                    def fake_urlopen(req, timeout=None):
                        captured.append(json.loads(req.data.decode("utf-8")))
                        payload = {
                            "choices": [{
                                "message": {"content": json.dumps({"ok": True})},
                                "finish_reason": "stop",
                            }],
                            "usage": {},
                            "model": "test-model",
                            "id": "test-response",
                        }
                        return io.BytesIO(json.dumps(payload).encode("utf-8"))

                    with patch("culturaeval.authentic_pilot.urllib.request.urlopen", side_effect=fake_urlopen):
                        result = request(case, condition, "test-model", "dummy-key-not-sent")

                    self.assertTrue(result["answer"]["ok"])
                    self.assertEqual(len(captured), 1)
                    messages = captured[0]["messages"]
                    prompt = messages[-1]["content"]
                    all_text = " ".join(m["content"] for m in messages)

                    self.assertIn(case["passage"], prompt)
                    self.assertNotIn("EXTERNAL CONTEXT [", all_text)
                    self.assertNotIn("Experimental adversarial note", all_text)
                    self.assertNotIn("NOT source fact", all_text)
                    self.assertNotIn("v2_condition_masked", all_text)
                    if condition == "passage_only":
                        self.assertNotIn("ADDITIONAL TEXTUAL CONTEXT:", prompt)
                    else:
                        self.assertIn("ADDITIONAL TEXTUAL CONTEXT:", prompt)
                        expected = case["contexts"][condition].removeprefix(
                            "Experimental adversarial note (NOT source fact): "
                        ).strip()
                        self.assertIn(expected, prompt)

    def test_model_request_has_no_condition_metadata(self):
        case = self.cases[0]
        captured = []

        def fake_urlopen(req, timeout=None):
            captured.append(json.loads(req.data.decode("utf-8")))
            return io.BytesIO(json.dumps({
                "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                "model": "test-model",
            }).encode("utf-8"))

        with patch("culturaeval.authentic_pilot.urllib.request.urlopen", side_effect=fake_urlopen):
            request(case, "misleading", "test-model", "dummy")
        self.assertEqual(set(captured[0]), {"model", "temperature", "response_format", "messages"})
        self.assertEqual(captured[0]["temperature"], 0)


if __name__ == "__main__":
    unittest.main()
