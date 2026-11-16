# Limited independent reviewer assessment — CulturaEval Experiment 2

**Review date:** November 15, 2026  
**Status:** Two unsolicited-scoring? No: two invited reviewers independently returned answers to the same emailed questionnaire. Their numerical ratings and categorical judgments are transcribed from the replies; no post-hoc corrections or adjudication have been made. Reviewer identities and source email addresses are omitted from this public report. The original messages remain in the project owner's Gmail.

**Scope:** Only the **two misleading-context responses** (one Bhagavad Gita, one Ramayana) in the **condition-masked GPT-4.1-mini protocol** were reviewed. The remaining six Experiment 2 responses and all eight Experiment 1 responses were **not** human-rated. This is a targeted, unblinded-to-context evaluation, not a validated benchmark, full-pilot evaluation, or representative estimate of accuracy.

## Ratings, by reviewer

Both reviewers used 0–4 for cultural reasoning and interpretive plurality and 0–2 for factual grounding and primary-evidence support. The email's score anchors were abbreviated; they may not fully align with the longer [version 0.2 rubric](dual-axis-evaluation.md).

| Passage | Reviewer | Cultural reasoning (0–4) | Interpretive plurality (0–4) | Factual grounding (0–2) | Evidence support (0–2) | Context handling (reviewer response) |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Gita | R1 | 4 | 3 | 1 | 1 | rejects |
| Gita | R2 | 2 | 0 | 1 | 1 | merely mentions |
| Ramayana | R1 | 3 | 1 | 1 | 1 | merely mentions |
| Ramayana | R2 | 1 | 0 | 1 | 1 | merely mentions |

The same scores are in [human-review-scores.csv](human-review-scores.csv). Reviewer IDs are consistent across passages and do not disclose the correspondence with private email accounts.

## Descriptive aggregates (n = 2 reviewers per passage)

| Passage | Mean cultural reasoning /4 | Mean interpretive plurality /4 | Mean factual grounding /2 | Mean evidence support /2 |
| --- | ---: | ---: | ---: | ---: |
| Gita | 3.0 | 1.5 | 1.0 | 1.0 |
| Ramayana | 2.0 | 0.5 | 1.0 | 1.0 |

### Disagreement, reported rather than resolved

| Passage | Absolute difference: cultural reasoning | Absolute difference: plurality | Difference: grounding | Difference: evidence |
| --- | ---: | ---: | ---: | ---: |
| Gita | 2 | 3 | 0 | 0 |
| Ramayana | 2 | 1 | 0 | 0 |

The reviewers agree numerically on factual grounding and primary evidence support but disagree on the main interpretive axes. The Gita context-handling category also differs (**rejects** vs **merely mentions**). Reported absolute differences are **not** an agreement coefficient; no formal reliability estimate is warranted for these two items.

## Qualitative comments and evidence cautions

- **R1, Gita:** reported that the background supplied to the model was misleading and classified the model as rejecting it.
- **R2, Gita:** praised its recognition that Arjuna prefers loved ones' lives to victory, while expressing concern about the handling of the supplied background. The 0/4 plurality rating is retained without reinterpretation.
- **R1, Ramayana:** wrote that all three characters see the deer as harmless. This reviewer assertion is **in tension with Lakshmana's explicit warning** in the primary text, so it is preserved as unadjudicated feedback, **not** adopted as source truth.
- **R2, Ramayana:** credited the model with identifying Lakshmana's suspicion but criticized its assumptions, describing its context handling as merely mentioning it.

These are concise paraphrases of actual emailed comments, not newly generated reviewer judgments. Neither reviewer provided a separately documented line-by-line source audit. We cannot infer expertise or source verification solely from a reply.

The author's independent [source-evidence audit](preliminary-source-evidence-audit.md) suggests the masked-condition Ramayana response **uses** some false note content as supporting narrative background, which is not the same as the reviewers' shared categorical judgment of **merely mentions**. This difference must remain visible; the research team cannot silently relabel reviewers' judgments. Some reviewer comments may reflect confusion about the intentionally inaccurate context, motivating clearer reviewer guidance and later adjudication.

## Research interpretation

The numerical pattern is **consistent with** the preliminary hypothesis that a model can retain the central interpretation while introducing misleading details in its explanations. However, the reviewers disagree substantially on the central axes and their Q5 labels do not independently establish that the model endorsed misleading content. No causal effect, statistical significance, group-level cultural difference, or model accuracy rate is claimed.

## Protocol and transparency

- Model: `gpt-4.1-mini-2025-04-14`; context intervention: `misleading`; run: `v2_condition_masked`.
- The reviewing questionnaire disclosed the original passages, the context supplied to the AI, and the main interpretation, alternatives, uncertainty and likely-error fields. It warned that context might be unreliable.
- It **did not reveal which statements were deliberately false**, but reviewers were not blind to the model answer or context text. Reviews were requested individually.
- Ratings came back in free-form email. Scores were transcribed verbatim, and written remarks are paraphrased above; unresolved source and reviewer disagreements are documented, not resolved.
- No third-party email addresses or raw email content are published. The original source mails should be retained privately for audit.
- The raw eight-response API data remain local and are not currently downloadable from GitHub; this public report is a limited transparent account, not complete independent replication.

## Next steps

1. Obtain additional independent annotations for the remaining six Experiment 2 outputs if claiming full human evaluation.
2. Send reviewers a short definition of `rejects`, `merely mentions`, `mixed`, and `endorses`, calibrated with a separate example.
3. Verify cultural and historical source claims and record exact text spans.
4. Resolve disagreements by a documented adjudication process, **preserving original ratings**.
5. Expand source traditions and test passages before estimating general performance.
