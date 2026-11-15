"""Human dual-axis evaluation data validation and summary.

This module does not infer human judgments from model answers.
It validates independently supplied reviewer ratings and summarizes them.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean

AXES = ("cultural_reasoning", "interpretive_plurality")
OTHER = ("factual_grounding", "primary_evidence_support")


def validate_annotation(row: dict) -> dict:
    """Return a validated copy of a single human annotation.

    Expected: passage_id, model_id, condition, reviewer_id,
    cultural_reasoning (0..4), interpretive_plurality (0..4),
    factual_grounding (0..2), primary_evidence_support (0..2).
    """
    required = ("passage_id", "model_id", "condition", "reviewer_id", *AXES, *OTHER)
    missing = [k for k in required if k not in row]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    for k in required[:4]:
        if not isinstance(row[k], str) or not row[k].strip():
            raise ValueError(f"{k} must be a nonempty string")
    if row["condition"] not in ("passage_only", "relevant", "partial", "misleading"):
        raise ValueError("Unknown context condition")
    for key in AXES:
        if type(row[key]) is not int or not 0 <= row[key] <= 4:
            raise ValueError(f"{key} must be an integer from 0 to 4")
    for key in OTHER:
        if type(row[key]) is not int or not 0 <= row[key] <= 2:
            raise ValueError(f"{key} must be an integer from 0 to 2")
    return dict(row)


def summarize_annotations(rows: list[dict]) -> list[dict]:
    """Per-model, per-condition mean scores; no imputation or adjudication."""
    valid = [validate_annotation(row) for row in rows]
    seen = set()
    for row in valid:
        key = tuple(row[k] for k in ("passage_id", "model_id", "condition", "reviewer_id"))
        if key in seen:
            raise ValueError(f"Duplicated annotation: {key}")
        seen.add(key)
    groups = defaultdict(list)
    for row in valid:
        groups[(row["model_id"], row["condition"])].append(row)
    result = []
    for (model, condition), group in sorted(groups.items()):
        result.append({
            "model_id": model,
            "condition": condition,
            "n_annotations": len(group),
            "n_unique_passages": len({r["passage_id"] for r in group}),
            **{f"mean_{axis}": round(mean(r[axis] for r in group), 3) for axis in (*AXES, *OTHER)},
        })
    return result


def reviewer_disagreement(rows: list[dict]) -> list[dict]:
    """Absolute two-reviewer differences per axis; not an agreement coefficient."""
    valid = [validate_annotation(row) for row in rows]
    groups = defaultdict(list)
    for row in valid:
        key = (row["passage_id"], row["model_id"], row["condition"])
        groups[key].append(row)
    results = []
    for key, group in sorted(groups.items()):
        if len(group) == 2 and group[0]["reviewer_id"] != group[1]["reviewer_id"]:
            results.append({
                "passage_id": key[0], "model_id": key[1], "condition": key[2],
                **{f"{axis}_absolute_difference": abs(group[0][axis] - group[1][axis]) for axis in AXES},
            })
    return results
