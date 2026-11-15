import unittest
from culturaeval.human_rubric import validate_annotation, summarize_annotations, reviewer_disagreement

BASE = {"passage_id": "P-001", "model_id": "example-model", "condition": "relevant",
        "reviewer_id": "A", "cultural_reasoning": 3, "interpretive_plurality": 4,
        "factual_grounding": 2, "primary_evidence_support": 2}

class TestHumanRubric(unittest.TestCase):
    def test_both_axes_are_distinct(self):
        row = validate_annotation(BASE)
        self.assertEqual(row["cultural_reasoning"], 3)
        self.assertEqual(row["interpretive_plurality"], 4)

    def test_invalid_scores_rejected(self):
        with self.assertRaises(ValueError):
            validate_annotation({**BASE, "interpretive_plurality": 5})
        with self.assertRaises(ValueError):
            validate_annotation({**BASE, "cultural_reasoning": True})

    def test_independent_reviewers(self):
        second = {**BASE, "reviewer_id": "B", "cultural_reasoning": 2, "interpretive_plurality": 1}
        summary = summarize_annotations([BASE, second])
        self.assertEqual(summary[0]["mean_cultural_reasoning"], 2.5)
        self.assertEqual(summary[0]["mean_interpretive_plurality"], 2.5)
        diff = reviewer_disagreement([BASE, second])[0]
        self.assertEqual(diff["cultural_reasoning_absolute_difference"], 1)
        self.assertEqual(diff["interpretive_plurality_absolute_difference"], 3)

    def test_duplicate_reviewer_not_double_counted(self):
        with self.assertRaises(ValueError):
            summarize_annotations([BASE, BASE])

if __name__ == "__main__":
    unittest.main()
