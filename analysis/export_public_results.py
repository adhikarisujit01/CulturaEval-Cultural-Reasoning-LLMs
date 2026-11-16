"""Build a privacy-minimized public pilot dataset from local API outputs.

Explicit allowlist excludes provider response IDs, token usage, credentials,
reviewer identities, and arbitrary unrecognized metadata. Does not publish data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CONDITIONS = {"passage_only", "relevant", "partial", "misleading"}
ANSWER_FIELDS = (
    "main_interpretation",
    "passage_evidence",
    "context_claims_used",
    "alternative_interpretations",
    "uncertainties",
    "likely_errors",
)

def load(path: Path, protocol: str) -> list[dict]:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("prompt_protocol", protocol) != protocol:
            raise ValueError(f"Protocol mismatch in {path} line {i}")
        if record["condition"] not in CONDITIONS:
            raise ValueError(f"Unexpected condition in {path} line {i}")
        if not isinstance(record["answer"], dict):
            raise ValueError(f"Missing answer in {path} line {i}")
        answer = {key: record["answer"][key] for key in ANSWER_FIELDS}
        if not all(isinstance(answer[key], str) for key in (
            "main_interpretation", "passage_evidence", "uncertainties", "likely_errors"
        )):
            raise ValueError(f"Unexpected answer field type in {path} line {i}")
        for key in ("context_claims_used", "alternative_interpretations"):
            if not isinstance(answer[key], list) or not all(isinstance(x, str) for x in answer[key]):
                raise ValueError(f"Unexpected list field in {path} line {i}")
        rows.append({
            "protocol": protocol,
            "case_id": record["case_id"],
            "condition": record["condition"],
            "model": record["provider_model"],
            "source_url": record["source_url"],
            "answer": answer,
        })
    if not rows:
        raise ValueError(f"No responses in {path}")
    return rows

def export(v1: Path, v2: Path, output: Path) -> None:
    records = load(v1, "v1_original") + load(v2, "v2_condition_masked")
    seen = set()
    coverage = {}
    for record in records:
        key = (record["protocol"], record["case_id"], record["condition"], record["model"])
        if key in seen:
            raise ValueError(f"Duplicate response: {key}")
        seen.add(key)
        pair = (record["protocol"], record["case_id"], record["model"])
        coverage.setdefault(pair, set()).add(record["condition"])
    for pair, conditions in coverage.items():
        if conditions != CONDITIONS:
            raise ValueError(f"Incomplete case: {pair}")
    if set(r["protocol"] for r in records) != {"v1_original", "v2_condition_masked"}:
        raise ValueError("Both protocols required")
    records.sort(key=lambda r: (r["protocol"], r["case_id"], r["condition"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Exported {len(records)} responses to {output}")
    print("ALLOWED FIELDS ONLY:", list(records[0]))
    print("This file has NOT been committed or published. Review it before uploading.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v1", default="results/authentic-pilot/gpt-4.1-mini/model_responses.jsonl")
    parser.add_argument("--v2", default="results/authentic-pilot-v2/gpt-4.1-mini/model_responses.jsonl")
    parser.add_argument("--output", default="results/public-review/culturaeval-model-responses.jsonl")
    args = parser.parse_args()
    export(Path(args.v1), Path(args.v2), Path(args.output))

if __name__ == "__main__":
    main()
