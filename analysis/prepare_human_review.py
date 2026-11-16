"""Prepare auditable, condition-masked review sheets from authentic pilot outputs.

No human judgment is inferred. Randomized review IDs do not expose condition names.
Because context may reveal the intervention, this is condition-label masking, not
guaranteed reviewer blinding. Keep the mapping file private.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path

CONDITIONS = {"passage_only", "relevant", "partial", "misleading"}
RATING_FIELDS = (
    "cultural_reasoning", "interpretive_plurality",
    "factual_grounding", "primary_evidence_support",
)
CONTEXT_LABELS = ("endorsed", "rejected", "mentioned_only", "mixed", "unclear", "not_applicable")

def prepare(input_file: Path, output_dir: Path, dataset_file: Path, seed: int = 2026) -> int:
    cases = {x['id']: x for x in (json.loads(line) for line in dataset_file.read_text(encoding='utf-8').splitlines() if line.strip())}

    rows = [json.loads(line) for line in input_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("No model responses found")
    seen = set()
    for row in rows:
        key = (row["case_id"], row["provider_model"], row["condition"])
        if row["condition"] not in CONDITIONS or key in seen:
            raise ValueError(f"Invalid or duplicate experimental condition: {key}")
        seen.add(key)
        answer = row["answer"]
        for k in ("main_interpretation", "passage_evidence", "context_claims_used",
                  "alternative_interpretations", "uncertainties", "likely_errors"):
            if k not in answer:
                raise ValueError(f"Missing answer field {k} for {key}")

    # IDs are opaque; no subject, condition, or ordering is embedded.
    rng = random.Random(seed)
    rng.shuffle(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    reviews, mapping = [], []
    for idx, row in enumerate(rows, 1):
        a = row["answer"]
        case = cases.get(row["case_id"])
        if case is None:
            raise ValueError(f"Missing source passage for {row['case_id']}")
        context = "(No external context provided.)" if row["condition"] == "passage_only" else case["contexts"][row["condition"]]
        rid = f"REV-{idx:03d}"
        reviews.append({
            "review_id": rid,
            "model_id": row["provider_model"],
            "source_passage": case["passage"],
            "context_provided_to_model": context,
            "main_interpretation": a["main_interpretation"],
            "passage_evidence": a["passage_evidence"],
            "context_claims_mentioned": json.dumps(a["context_claims_used"], ensure_ascii=False),
            "alternative_interpretations": json.dumps(a["alternative_interpretations"], ensure_ascii=False),
            "uncertainties": a["uncertainties"],
            "likely_errors": a["likely_errors"],
            "reviewer_id": "",
            **{field: "" for field in RATING_FIELDS},
            "context_claim_disposition": "",
            "evidence_support_notes": "",
            "reviewer_notes": "",
        })
        mapping.append({
            "review_id": rid, "passage_id": row["case_id"],
            "model_id": row["provider_model"], "condition": row["condition"],
            "response_id": row.get("response_id", ""),
            "source_url": row.get("source_url", ""),
        })
    def write_csv(path, data):
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

    write_csv(output_dir / "review_sheet.csv", reviews)
    write_csv(output_dir / "PRIVATE_condition_key.csv", mapping)
    (output_dir / "README.txt").write_text(
        "Review each response using docs/dual-axis-evaluation.md.\n"
        "Use independent reviewer IDs; make a separate copy of review_sheet.csv per reviewer.\n"
        "Context claim disposition: " + ", ".join(CONTEXT_LABELS) + ".\n"
        "For passage_only choose not_applicable. For other conditions note whether\n"
        "context claims were endorsed, rejected, only mentioned, mixed, or unclear.\n"
        "Ratings must be completed by human reviewers; no auto-scoring is performed.\n"
        "WARNING: The supplied-context wording may reveal experimental conditions.\n"
        "This sheet masks condition labels only; it cannot guarantee full blinding.\n"
        "Use PRIVATE_condition_key.csv only after reviewing. Do NOT publish identifiable\n"
        "reviewer comments or the private key without checking release suitability.\n",
        encoding="utf-8",
    )
    return len(rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="results/authentic-pilot/gpt-4.1-mini/model_responses.jsonl")
    parser.add_argument("--output", default="results/authentic-pilot/human-review")
    parser.add_argument("--dataset", default="data/authentic_pilot_candidates.jsonl")
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    total = prepare(Path(args.input), Path(args.output), Path(args.dataset), args.seed)
    print(f"Prepared {total} condition-label-masked records in {args.output}")
    print("All human rating fields left blank. Keep PRIVATE_condition_key.csv local.")

if __name__ == "__main__":
    main()
