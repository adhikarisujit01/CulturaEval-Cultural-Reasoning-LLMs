"""Experiment validation, prompt control, and evaluation methods (stdlib only)."""
from __future__ import annotations
import json
import random
import statistics
from pathlib import Path

CONDITIONS = ('passage_only', 'relevant', 'partial', 'misleading')
LABELS = ('ritual', 'irony', 'hospitality', 'grief', 'status', 'migration', 'memory', 'resistance', 'kinship', 'ambiguity')


def load_cases(path: str | Path) -> list[dict]:
    with open(path, encoding='utf-8') as f:
        cases = [json.loads(line) for line in f if line.strip()]
    ids = set()
    for case in cases:
        assert case['id'] not in ids, f"duplicate id: {case['id']}"
        ids.add(case['id'])
        assert case['primary_label'] in LABELS
        assert case['alternative_label'] in LABELS
        assert case['primary_label'] != case['alternative_label']
        assert all(k in case['contexts'] for k in ('relevant', 'partial', 'misleading'))
        assert case['passage'].strip() and case['evidence_quote'] in case['passage']
        assert case['provenance'] == 'synthetic_constructed_fixture'
    return cases


def build_messages(case: dict, condition: str) -> list[dict]:
    if condition not in CONDITIONS:
        raise ValueError(f'Unsupported condition: {condition}')
    supplied = '(No external context provided.)' if condition == 'passage_only' else case['contexts'][condition]
    system = ("You are a research assistant interpreting a short literary passage. "
              "The external note may be irrelevant, incomplete, or misleading. Do not treat it as authoritative. "
              "Ground claims in the passage, distinguish external notes from passage evidence, "
              "allow an alternative interpretation, and acknowledge uncertainty. "
              "Return ONLY a JSON object with these exact keys: "
              "interpretation_label (one of: " + ', '.join(LABELS) + "), "
              "interpretation (string), passage_evidence (exact short substring from passage), "
              "context_used (boolean), alternative_interpretation (string), confidence (number between 0 and 1).")
    user = f"PASSAGE:\n{case['passage']}\n\nEXTERNAL NOTE [{condition}]:\n{supplied}\n\nInterpret the passage."
    return [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]


def parse_response(text: str) -> dict:
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[-1].rsplit('```', 1)[0].strip()
    value = json.loads(text)
    required = {'interpretation_label', 'interpretation', 'passage_evidence', 'context_used', 'alternative_interpretation', 'confidence'}
    if not isinstance(value, dict) or not required.issubset(value):
        raise ValueError('Response missing required fields')
    if value['interpretation_label'] not in LABELS:
        raise ValueError('Unknown interpretation label')
    if type(value['context_used']) is not bool:
        raise ValueError('context_used must be boolean')
    if not isinstance(value['confidence'], (int, float)) or isinstance(value['confidence'], bool) or not (0 <= value['confidence'] <= 1):
        raise ValueError('confidence outside [0,1]')
    if any(not isinstance(value[k], str) for k in ('interpretation', 'passage_evidence', 'alternative_interpretation')):
        raise ValueError('Text field expected')
    return value


def score(case: dict, condition: str, response: dict) -> dict:
    accurate = int(response['interpretation_label'] == case['primary_label'])
    span_valid = int(bool(response['passage_evidence']) and response['passage_evidence'] in case['passage'])
    conf = response['confidence']
    return {
        'case_id': case['id'], 'family_id': case['family_id'], 'condition': condition,
        'accuracy_on_constructed_label': accurate,
        'evidence_span_present': span_valid,
        'overconfident_error': int(not accurate and conf >= 0.8),
        'brier_score': round((conf - accurate) ** 2, 6),
        'confidence': conf,
        'context_used_reported': int(response['context_used']),
        'alternative_present': int(bool(response['alternative_interpretation'].strip())),
    }


def summarize(scores: list[dict]) -> dict:
    output = {}
    for condition in CONDITIONS:
        subset = [s for s in scores if s['condition'] == condition]
        if not subset:
            continue
        output[condition] = {'n': len(subset)}
        for key in ('accuracy_on_constructed_label', 'evidence_span_present', 'overconfident_error', 'brier_score', 'confidence', 'context_used_reported', 'alternative_present'):
            output[condition][key] = round(statistics.mean(s[key] for s in subset), 4)
    return output


def paired_bootstrap(scores: list[dict], comparison: str, reference: str = 'passage_only', iterations: int = 2000, seed: int = 2026) -> dict:
    """Case-paired resampling for accuracy difference; illustrative on synthetic fixtures."""
    per = {}
    for s in scores:
        per.setdefault(s['case_id'], {})[s['condition']] = s
    keys = sorted(k for k, v in per.items() if comparison in v and reference in v)
    if not keys:
        raise ValueError('No matched cases')
    families = {}
    for k in keys:
        family = per[k][comparison]['family_id']
        families.setdefault(family, []).append(
            per[k][comparison]['accuracy_on_constructed_label'] - per[k][reference]['accuracy_on_constructed_label'])
    cluster_means = [statistics.mean(v) for _, v in sorted(families.items())]
    rng = random.Random(seed)
    trials = [statistics.mean(cluster_means[rng.randrange(len(cluster_means))] for _ in range(len(cluster_means))) for _ in range(iterations)]
    trials.sort()
    return {'comparison': comparison, 'reference': reference, 'n_paired_cases': len(keys),
            'n_motif_clusters': len(cluster_means),
            'difference': round(statistics.mean(cluster_means), 4),
            'cluster_bootstrap_95_interval': [round(trials[int(.025 * iterations)], 4), round(trials[min(iterations - 1, int(.975 * iterations))], 4)],
            'warning': 'Cluster bootstrap is only a pipeline demonstration; synthetic motifs do not justify population inference.'}
