"""Generate descriptive pilot table, SVG figure and Markdown report; no inferred human scores."""
import argparse
import csv
import html
import json
from collections import defaultdict
from pathlib import Path

CONDITIONS = ("passage_only", "relevant", "partial", "misleading")

def generate(source, output):
    rows = [json.loads(line) for line in Path(source).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("Missing responses")
    seen = set()
    groups = defaultdict(list)
    for row in rows:
        key = (row["case_id"], row["provider_model"], row["condition"])
        if key in seen or row["condition"] not in CONDITIONS:
            raise ValueError("Duplicate or unrecognized condition: " + str(key))
        seen.add(key)
        groups[row["condition"]].append(row)
    by_pair = defaultdict(set)
    for row in rows:
        by_pair[(row["case_id"], row["provider_model"])].add(row["condition"])
    if any(conditions != set(CONDITIONS) for conditions in by_pair.values()):
        raise ValueError("Some passages have missing conditions")
    summary = []
    for cond in CONDITIONS:
        group = groups[cond]
        summary.append({
            "condition": cond,
            "responses": len(group),
            "claims_listed": sum(len(x["answer"]["context_claims_used"]) for x in group),
            "alternatives_listed": sum(len(x["answer"]["alternative_interpretations"]) for x in group),
            "tokens": sum(x["usage"]["prompt_tokens"] + x["usage"]["completion_tokens"] for x in group)
        })
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    bar_max = max(1, *(r["claims_listed"] for r in summary))
    bars = []
    for i, r in enumerate(summary):
        yy = 85 + i * 65
        w = round(450 * r["claims_listed"] / bar_max)
        bars += [
            '<text x="15" y="' + str(yy + 25) + '">' + html.escape(r["condition"]) + '</text>',
            '<rect x="180" y="' + str(yy) + '" width="' + str(w) + '" height="36" fill="#557bad" rx="4"/>',
            '<text x="' + str(190 + w) + '" y="' + str(yy + 25) + '">' + str(r["claims_listed"]) + '</text>',
        ]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 400" width="760" height="400" role="img" aria-label="Listed context claims by condition">'
           '<rect width="100%" height="100%" fill="white"/>'
           '<g font-family="sans-serif" font-size="15" fill="#202020">'
           '<text x="15" y="35" font-weight="bold" font-size="20">Context claims listed in output</text>'
           + ''.join(bars) +
           '<text x="15" y="375" font-size="12">Mentions are not endorsement or accuracy scores; two passages only.</text>'
           '</g></svg>')
    (out / "claims.svg").write_text(svg, encoding="utf-8")
    md = [
        "# CulturaEval — exploratory authentic-text pilot",
        "",
        "**Scope:** Two historical-translation passages, four evidence conditions each, one real-model response per condition. Not a validated benchmark.",
        "",
        "Model version(s): " + ", ".join(sorted({r["provider_model"] for r in rows})),
        "",
        "| Condition | Responses | Listed context claims | Listed alternatives | Tokens |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in summary:
        md.append("| {condition} | {responses} | {claims_listed} | {alternatives_listed} | {tokens} |".format(**r))
    md += [
        "",
        "![Count of context claims listed](claims.svg)",
        "",
        "## Observations requiring independent evaluation",
        "",
        "The Gita outputs retain a core interpretation about moral conflict across conditions. The Ramayana outputs describe Lakshmana's suspicion; the misleading-context answer notes a contradiction with the provided note. These are tentative qualitative observations, not human-rated scores.",
        "",
        "## Interpretation and limitations",
        "",
        "A claim appearing in the context_claims_used field is not evidence that the model endorsed it. Neither cultural accuracy nor interpretive plurality has been independently rated.",
        "",
        "The notes were curated rather than automatically retrieved, and have not been independently authenticated. There are only two passages and no repeated samples. No significance tests, general retrieval effects, or population-level conclusions are justified.",
        "",
        "## Next research steps",
        "",
        "Independently check source citations and evidence notes; request two reviewers for each response; preserve pre-adjudication ratings and disagreements; expand passages and models; characterize actual retrieval algorithms before making retrieval-effect claims.",
        "",
        "Reproduce locally: python3 analysis/report_pilot.py",
        "",
        "The saved raw responses remain local unless intentionally published after review.",
    ]
    (out / "REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Generated", out / "REPORT.md", out / "summary.csv", out / "claims.svg", sep="\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="results/authentic-pilot/gpt-4.1-mini/model_responses.jsonl")
    p.add_argument("--output", default="results/authentic-pilot/report")
    args = p.parse_args()
    generate(args.input, args.output)

if __name__ == "__main__":
    main()
