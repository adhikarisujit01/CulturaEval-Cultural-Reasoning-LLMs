import csv
import json
from pathlib import Path

INPUT = Path(
    "results/authentic-pilot/gpt-4.1-mini/model_responses.jsonl"
)
OUTPUT = Path("results/authentic-pilot/pilot_comparison.csv")

rows = [
    json.loads(line)
    for line in INPUT.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

if len(rows) != 8:
    raise ValueError(f"Expected 8 responses, found {len(rows)}")

conditions = {"passage_only", "relevant", "partial", "misleading"}
by_case = {}

for row in rows:
    key = (row["case_id"], row["condition"])
    if key in by_case:
        raise ValueError(f"Duplicate response: {key}")
    by_case[key] = row

case_ids = sorted({r["case_id"] for r in rows})
for case_id in case_ids:
    actual = {c for (i, c) in by_case if i == case_id}
    if actual != conditions:
        raise ValueError(f"Incomplete conditions for {case_id}")

output_rows = []

for case_id in case_ids:
    for condition in (
        "passage_only", "relevant", "partial", "misleading"
    ):
        row = by_case[(case_id, condition)]
        answer = row["answer"]

        output_rows.append({
            "case_id": case_id,
            "condition": condition,
            "model": row["provider_model"],
            "interpretation": answer["main_interpretation"],
            "context_claim_count": len(
                answer["context_claims_used"]
            ),
            "alternative_count": len(
                answer["alternative_interpretations"]
            ),
            "uncertainty_reported": bool(
                answer["uncertainties"].strip()
            ),
            "prompt_tokens": row["usage"]["prompt_tokens"],
            "completion_tokens": row["usage"]["completion_tokens"],
            "human_cultural_score": "",
            "human_plurality_score": "",
            "human_context_endorsement": "",
        })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=output_rows[0])
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Analyzed {len(output_rows)} responses")
print(f"Saved: {OUTPUT}")
print("\nObservable metrics by condition:")

for condition in (
    "passage_only", "relevant", "partial", "misleading"
):
    subset = [
        r for r in output_rows
        if r["condition"] == condition
    ]
    total_claims = sum(r["context_claim_count"] for r in subset)
    alternatives = sum(r["alternative_count"] for r in subset)
    tokens = sum(
        r["prompt_tokens"] + r["completion_tokens"]
        for r in subset
    )
    print(
        f"{condition:14s} | "
        f"context mentions: {total_claims:2d} | "
        f"alternatives: {alternatives:2d} | "
        f"tokens: {tokens}"
    )

print("\nHuman-evaluation fields intentionally left blank.")
