"""Prepare claim-level evidence-audit worksheets from saved model responses.

This is a *human annotation template*, not an automated fact checker.
Each model-listed context claim is one audit candidate, and each response also
has an interpretation row. Model-supplied lists may contain compound claims:
reviewers must split them manually before treating records as atomic claims.

The public output has a stable response key but never includes credentials.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

FIELD_NAMES = (
    "audit_id", "case_id", "model_id", "condition", "prompt_protocol",
    "claim_kind", "candidate_claim", "passage", "source_url",
    "reviewer_id", "claim_atomicity", "evidence_status", "model_stance",
    "supporting_quote", "source_location", "reviewer_rationale",
)
EVIDENCE_STATUSES = (
    "supported_by_passage", "supported_by_verified_external_source",
    "contradicted_by_passage", "contradicted_by_verified_external_source",
    "not_established", "not_applicable",
)
MODEL_STANCES = (
    "endorsed", "rejected", "mentioned_without_endorsement",
    "mixed", "unclear", "not_applicable",
)

def generate(source: Path, dataset: Path, output: Path) -> int:
    cases = {
        case["id"]: case
        for line in dataset.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for case in [json.loads(line)]
    }
    responses = [
        json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not responses:
        raise ValueError("No responses found")
    seen = set()
    entries = []
    for response in responses:
        case_id = response["case_id"]
        if case_id not in cases:
            raise ValueError("Unknown case: " + case_id)
        model = response["provider_model"]
        condition = response["condition"]
        protocol = response.get("prompt_protocol", "v1_unlabeled")
        key = (case_id, model, condition, protocol)
        if key in seen:
            raise ValueError(f"Duplicate response: {key}")
        seen.add(key)
        source_case = cases[case_id]
        answer = response["answer"]
        claims = [("main_interpretation", answer["main_interpretation"])]
        claims += [("context_claim_list_item", text) for text in answer["context_claims_used"]]
        claims += [("alternative_interpretation", text) for text in answer["alternative_interpretations"]]
        claims += [("uncertainties", answer["uncertainties"])]
        claims += [("likely_errors", answer["likely_errors"])]
        for number, (kind, claim) in enumerate(claims, 1):
            if not isinstance(claim, str) or not claim.strip():
                continue
            stable = json.dumps([case_id, model, condition, protocol, kind, number], ensure_ascii=False)
            audit_id = hashlib.sha256(stable.encode("utf-8")).hexdigest()[:12]
            entries.append({
                "audit_id": audit_id,
                "case_id": case_id,
                "model_id": model,
                "condition": condition,
                "prompt_protocol": protocol,
                "claim_kind": kind,
                "candidate_claim": claim,
                "passage": source_case["passage"],
                "source_url": source_case["source_url"],
                "reviewer_id": "",
                "claim_atomicity": "",
                "evidence_status": "",
                "model_stance": "",
                "supporting_quote": "",
                "source_location": "",
                "reviewer_rationale": "",
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(entries)
    print(f"Prepared {len(entries)} unscored audit candidates from {len(responses)} responses")
    print("Saved:", output)
    print("All reviewer fields remain blank")
    return len(entries)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="results/authentic-pilot-v2/gpt-4.1-mini/model_responses.jsonl")
    parser.add_argument("--dataset", default="data/authentic_pilot_candidates.jsonl")
    parser.add_argument("--output", default="results/authentic-pilot-v2/claim-audit/claim_audit.csv")
    args = parser.parse_args()
    generate(Path(args.input), Path(args.dataset), Path(args.output))

if __name__ == "__main__":
    main()
