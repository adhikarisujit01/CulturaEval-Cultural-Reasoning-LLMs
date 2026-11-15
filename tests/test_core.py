import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from culturaeval.core import CONDITIONS, build_messages, load_cases, parse_response, score, summarize, paired_bootstrap
from culturaeval.runner import demo_response, run

DATA = Path(__file__).resolve().parents[1] / 'data' / 'synthetic_cases.jsonl'

class TestBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(DATA)

    def test_dataset_count_and_family_structure(self):
        self.assertEqual(len(self.cases), 40)
        self.assertEqual(len({c['family_id'] for c in self.cases}), 10)

    def test_all_prompt_conditions(self):
        case = self.cases[0]
        for condition in CONDITIONS:
            text = build_messages(case, condition)[1]['content']
            self.assertIn(case['passage'], text)
            if condition == 'passage_only':
                self.assertIn('No external context provided', text)
            else:
                self.assertIn(case['contexts'][condition], text)

    def test_invalid_prompt_condition(self):
        with self.assertRaises(ValueError):
            build_messages(self.cases[0], 'secret_gold')

    def test_structured_answer_validation(self):
        case = self.cases[0]
        answer = parse_response(json.dumps(demo_response(case, 'relevant')))
        self.assertTrue(0 <= answer['confidence'] <= 1)
        with self.assertRaises(ValueError):
            parse_response('{}')
        bad = {**answer, 'confidence': 2.0}
        with self.assertRaises(ValueError):
            parse_response(json.dumps(bad))

    def test_scoring_rejects_fabricated_evidence_span(self):
        case = self.cases[0]
        response = {**demo_response(case, 'relevant'), 'passage_evidence':'made-up passage text'}
        self.assertEqual(score(case, 'relevant', response)['evidence_span_present'], 0)

    def test_deterministic_demo(self):
        case = self.cases[0]
        self.assertEqual(demo_response(case, 'misleading'), demo_response(case, 'misleading'))

    def test_paired_cluster_bootstrap(self):
        scores = [score(c, cond, demo_response(c, cond)) for c in self.cases for cond in CONDITIONS]
        self.assertEqual(summarize(scores)['relevant']['n'], 40)
        result = paired_bootstrap(scores, 'relevant')
        self.assertEqual(result['n_paired_cases'], 40)
        self.assertEqual(result['n_motif_clusters'], 10)

    def test_end_to_end(self):
        with TemporaryDirectory() as directory:
            report = run(DATA, Path(directory), 'demo', None, '', 4)
            self.assertEqual(report['successful_predictions'], 16)
            self.assertEqual(report['total_cases'], 4)
            self.assertEqual(len(report['failures']), 0)
            self.assertTrue((Path(directory) / 'report.json').exists())
            self.assertIn('NOT RESEARCH RESULTS', report['result_type'])

if __name__ == '__main__':
    unittest.main()
