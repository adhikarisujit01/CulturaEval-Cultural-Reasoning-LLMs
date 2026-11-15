# Dual-axis human evaluation protocol — version 0.2

**Status:** Proposed evaluation design. No human-annotated benchmark or real-model results have been validated yet.

## Core research question

When does adding external cultural or historical context improve a language model's **culturally grounded interpretation**, and when does it improve or degrade the model's ability to **recognize competing defensible interpretations**?

These are **two distinct outcomes**. A model may accurately identify one culturally supported reading but still incorrectly declare it the only possible reading. Conversely, a model may list many alternative readings but fail to recognize the most strongly supported cultural context.

## Axis A — Cultural reasoning (0–4; human-rated)

- **0:** Fundamental misunderstanding of culturally relevant actions, terms, or obligations, or unsupported invented cultural facts.
- **1:** Recognizes superficial topic but misstates key cultural or narrative relationships.
- **2:** Partially grounded interpretation with important missing cultural details or unsupported claims.
- **3:** Substantially accurate interpretation, grounded in passage and verified cultural context, with minor limitations.
- **4:** Precise contextual reasoning tied to specific textual evidence; carefully separates source assertions, inference, and uncertainty.

### Evidence checks (separate)

Record whether quoted material exists verbatim; whether the quote *actually supports* the interpretation; and whether the model correctly attributes retrieved contextual material. A valid substring alone is **not** evidence-grounding success.

## Axis B — Interpretive plurality (0–4; human-rated)

- **0:** Unjustifiably asserts a single definitive interpretation, or lists clearly implausible readings without critique.
- **1:** Mentions an alternative but treats it as filler, caricatures it, or refuses to distinguish evidence strengths.
- **2:** Identifies at least one plausible competing reading with some evidence or reservation.
- **3:** Presents multiple defensible readings, notes textual constraints, and weighs competing evidence appropriately.
- **4:** Carefully explains which readings are warranted by the available text, what contextual evidence changes their standing, and where ambiguity genuinely remains.

A high score does **not** require manufacturing ambiguity in a straightforward passage. If experts agree the text supports only one reading, identifying *why other readings fail* can earn 4. The human annotation must first describe the passage's genuine ambiguity level.

## Additional outcomes

- Factual grounding of the cited historical/cultural claims (0–2)
- Source-evidence support of the primary reading (0–2)
- Hallucinated or contradicted source claims (binary)
- Confidence calibration (model-reported uncertainty and empirically assessed correctness; do not infer probabilities from verbal hedges)
- Harmful stereotyping or sweeping generalization (flag for review)

**Do not collapse the two axes into one score for the primary analysis.** Report each independently, with sensitivity analyses as appropriate.

## Context intervention

Evaluate each unchanged passage under: (1) no added note, (2) verified relevant note, (3) partial but accurate note, (4) plausible contradictory/misleading note. Preserve identical model instructions except for the context. Counterbalance order and separate passage authoring from model scoring where practical.

## Expert annotation

1. Assign passage and source IDs; retain exact edition, verse/chapter, translation and license.
2. Produce an evidence-linked cultural interpretation guide. Record *what is known*, *what is debated*, and *what remains underdetermined*.
3. Obtain two independent reviewer ratings for both axes while concealing model identity and retrieval condition when possible.
4. Resolve disagreements with written adjudication, retain pre-adjudication scores, and report agreement.
5. Do not assume a single Nepali/Hindu insider interpretation is universally authoritative: textual traditions and commentaries may conflict.

## Analysis

For each model, compare paired scores for each passage across the four retrieval conditions. Summarize axis A and B separately with reviewer uncertainty. Cluster any resampling at the narrative episode/source-family level rather than assuming near-duplicate passages are independent. Report effect sizes, confidence intervals, disagreement, and failure examples. Avoid formal inferential claims from the current synthetic fixtures.

## Illustrative contrast

A model may understand Yudhishthira's reply to the Yaksha as involving duty and kinship, yet overlook how alternative ethical frameworks prioritize different obligations. Another may offer many possible readings but invent a historical norm. This illustrates the rubric only; no episode is included as a validated benchmark item until the exact passage and edition are verified.

## Current reproducibility status

The existing `data/synthetic_cases.jsonl` consists of fictional software-test fixtures, not an expert gold standard. Existing automated scoring is useful for code checks but **does not measure either human-evaluated axis**. Use `culturaeval/human_rubric.py` to validate and summarize human annotations once real model outputs and verified source passages exist.
