"""Run demo fixtures or optional OpenAI-compatible API models."""
from __future__ import annotations
import argparse
import json
import os
import random
import time
import urllib.request
from pathlib import Path
from .core import CONDITIONS, build_messages, load_cases, parse_response, score, summarize, paired_bootstrap


def demo_response(case: dict, condition: str) -> dict:
    """Deterministic test double, NOT a language-model result or research evidence."""
    rng = random.Random(f"{case['id']}:{condition}:2026")
    probability = {'passage_only': .43, 'relevant': .81, 'partial': .55, 'misleading': .26}[condition]
    label = case['primary_label'] if rng.random() < probability else case['alternative_label']
    conf = .85 if condition == 'misleading' else (.78 if condition == 'relevant' else .64)
    return {'interpretation_label': label, 'interpretation': f"Demonstration-only selection: {label}.",
            'passage_evidence': case['evidence_quote'], 'context_used': condition != 'passage_only',
            'alternative_interpretation': f"Alternative reading: {case['alternative_label']}.",
            'confidence': conf}


def api_response(case: dict, condition: str, model: str, endpoint: str, key: str) -> dict:
    """Explicit opt-in network request: OpenAI-compatible chat completions JSON mode."""
    payload = {'model': model, 'temperature': 0, 'messages': build_messages(case, condition),
               'response_format': {'type': 'json_object'}}
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode('utf-8'), method='POST',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = json.load(r)
    return parse_response(body['choices'][0]['message']['content'])


def run(dataset: Path, output: Path, backend: str, model: str | None, endpoint: str, limit: int | None) -> dict:
    cases = load_cases(dataset)
    if limit:
        cases = cases[:limit]
    if backend == 'api' and not (model and os.environ.get('CULTURAEVAL_API_KEY')):
        raise ValueError('API backend needs --model and CULTURAEVAL_API_KEY')
    output.mkdir(parents=True, exist_ok=True)
    predictions, scores, failures = [], [], []
    for case in cases:
        for condition in CONDITIONS:
            try:
                response = (demo_response(case, condition) if backend == 'demo' else
                            api_response(case, condition, model, endpoint, os.environ['CULTURAEVAL_API_KEY']))
                if backend == 'api':
                    response = parse_response(json.dumps(response))
                row = {'case_id': case['id'], 'condition': condition, 'backend': backend,
                       'model': model if backend == 'api' else 'DETERMINISTIC_TEST_DOUBLE_NOT_LLM', 'response': response}
                predictions.append(row)
                scores.append(score(case, condition, response))
            except Exception as exc:
                failures.append({'case_id': case['id'], 'condition': condition, 'error': str(exc)[:300]})
            if backend == 'api':
                time.sleep(0.2)
    with (output / 'predictions.jsonl').open('w', encoding='utf-8') as f:
        for row in predictions:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    with (output / 'scores.jsonl').open('w', encoding='utf-8') as f:
        for row in scores:
            f.write(json.dumps(row) + '\n')
    comparisons = []
    for condition in CONDITIONS[1:]:
        try:
            comparisons.append(paired_bootstrap(scores, condition))
        except ValueError:
            pass
    report = {'provenance': 'synthetic constructed prompts and contexts',
              'result_type': 'INFRASTRUCTURE SMOKE TEST — NOT RESEARCH RESULTS' if backend == 'demo' else 'EXPLORATORY LLM RESULTS ON SYNTHETIC FIXTURES',
              'model': model if backend == 'api' else None, 'total_cases': len(cases), 'successful_predictions': len(predictions),
              'failures': failures, 'metrics': summarize(scores), 'paired_differences': comparisons,
              'limitations': ['Constructed benchmark is not culturally validated', 'Gold labels reflect test author assumptions',
                              'Exact quote checks do not prove interpretation grounding', 'No independent human annotations']}
    (output / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset', type=Path, default=Path(__file__).resolve().parents[1] / 'data' / 'synthetic_cases.jsonl')
    p.add_argument('--output', type=Path, default=Path('results/demo'))
    p.add_argument('--backend', choices=['demo', 'api'], default='demo')
    p.add_argument('--model', help='Required for API backend; model name of your provider')
    p.add_argument('--endpoint', default='https://api.openai.com/v1/chat/completions', help='OpenAI-compatible endpoint')
    p.add_argument('--limit', type=int, default=None)
    a = p.parse_args()
    print(json.dumps(run(a.dataset, a.output, a.backend, a.model, a.endpoint, a.limit), indent=2))

if __name__ == '__main__':
    main()
