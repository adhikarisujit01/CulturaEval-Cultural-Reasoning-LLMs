"""Summarize published CulturaEval responses without requiring original API metadata.

No inference of cultural accuracy or context endorsement is attempted.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path

CONDITIONS = {"passage_only", "relevant", "partial", "misleading"}

def summarize(source: Path, output: Path) -> None:
    rows = [json.loads(s) for s in source.read_text(encoding="utf-8").splitlines() if s.strip()]
    seen = set()
    grouped = collections.defaultdict(list)
    coverage = collections.defaultdict(set)
    for r in rows:
        key = (r["protocol"], r["case_id"], r["condition"], r["model"])
        if r["condition"] not in CONDITIONS or key in seen:
            raise ValueError(f"Unexpected or duplicate record {key}")
        seen.add(key)
        coverage[(r["protocol"], r["case_id"], r["model"])].add(r["condition"])
        grouped[(r["protocol"], r["condition"])].append(r)
    if not rows or any(x != CONDITIONS for x in coverage.values()):
        raise ValueError("Dataset is empty or a passage is missing conditions")
    summary = []
    for (protocol, condition), group in sorted(grouped.items()):
        summary.append({
            "protocol": protocol,
            "condition": condition,
            "n_responses": len(group),
            "n_passages": len({r["case_id"] for r in group}),
            "listed_context_claims": sum(len(r["answer"]["context_claims_used"]) for r in group),
            "listed_alternatives": sum(len(r["answer"]["alternative_interpretations"]) for r in group),
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Verified {len(rows)} responses across {len(coverage)} protocol/passage/model pairs")
    print(f"Wrote {output}")
    print("These are descriptive counts, NOT evidence of endorsement or cultural correctness.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/experimental-results/model-responses.jsonl")
    parser.add_argument("--output", default="results/public-review/descriptive-summary.csv")
    args = parser.parse_args()
    summarize(Path(args.input), Path(args.output))

if __name__ == "__main__":
    main()
