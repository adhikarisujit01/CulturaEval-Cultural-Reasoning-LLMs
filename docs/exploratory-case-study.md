# CulturaEval: exploratory case study of misleading context

**Status:** Authorial qualitative inspection only. No independent human or expert ratings have been collected. This is not a validated benchmark.

## Question

Can a model preserve a plausible main interpretation of a cultural text while allowing unsupported external context to alter its secondary reasoning?

## Setup

Two English translated passages: Bhagavad Gita Chapter II (Edwin Arnold) and Ramayana Aranya Kanda XLIII (Manmatha Nath Dutt), each under four curated context conditions. Two GPT-4.1-mini runs: original pilot and a later condition-label-masked protocol. There was one response per case and condition in each run. Inputs are in [authentic_pilot_candidates.jsonl](../data/authentic_pilot_candidates.jsonl). Local outputs are not yet published in the repository, so the observations below cannot currently be independently reproduced from the repository alone.

## Observations: misleading-context responses only

| Passage | Original protocol | Masked-condition protocol |
| --- | --- | --- |
| Gita | Main interpretation identifies Arjuna's moral conflict; the response's likely-errors field expressly rejects the false claims about strangers and lack of training. | Main interpretation still identifies a moral conflict. The response identifies the contradictory context but entertains military training as an alternative possibility. |
| Ramayana | Main interpretation identifies Lakshmana's suspicion that the deer is Māricha and notes conflict between that suspicion and the supplied harmless-deer note. | Main interpretation still identifies Lakshmana's suspicion but also characterizes a prior shared belief that the deer was harmless, from the false note. In likely-errors, the response uses this note to undermine the idea that Lakshmana had prior knowledge of Māricha. |

Illustrative model-output quotations (not primary-source statements):

- Masked Gita: “conflicts with the passage's emphasis on their honor and his love for them.”
- Masked Ramayana: “despite the characters' prior belief that the deer is harmless.”
- Masked Ramayana likely-errors: “contradicts the additional context stating the deer is ordinary and recognized as harmless.”

These examples suggest a hypothesis of **secondary-reasoning contamination**: a broadly appropriate main answer may coexist with unsupported claims in explanation and uncertainty statements. The hypothesis is not a rate estimate or causal conclusion.

## Interpretation boundaries

A claim listed in the output field `context_claims_used` may be endorsed, rejected or merely mentioned. No endorsement judgment should rely solely on its appearance in that list. Full response text, original passage and independently checked evidence are required.

The two prompting protocols differ in more than whether they identify the condition; the comparison does not isolate a single causal factor. Sample size is two source passages from related cultural traditions; both were accessed through historical English translations. No repeated model samples, source-expert validation, independently annotated reviewer ratings, or population-level inference are available. The intervention is **curated context**, not an implemented retrieval ranking system.

## Reproduction and validation path

1. Record and preserve the exact prompt protocol and model version for every run.
2. Validate passage provenance and individual context claims against reliable sources.
3. Split compound model assertions into atomic claims and record quoted evidence.
4. Obtain independent reviewers' cultural reasoning and interpretive plurality scores, retaining disagreements.
5. Repeat across more passages, culturally diverse sources, models and samples. Do not interpret tokens or claim-mention counts as accuracy.

This case study deliberately reports preliminary qualitative observations rather than fabricated quantitative scores.
