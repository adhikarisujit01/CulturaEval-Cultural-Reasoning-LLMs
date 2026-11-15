# CulturaEval: experimental methodology

## Hypothesis

Context-aware interpretation of culturally situated literary material may improve with relevant retrieval but deteriorate when retrieved material is incomplete, unverified or misleading. An accurate experiment must also accommodate genuinely ambiguous readings, rather than assuming every passage has a single definitive interpretation.

## Design

Each passage is evaluated under four conditions:

1. Passage only, without external notes.
2. Relevant external note.
3. Partially informative, non-dispositive note.
4. Plausible but deliberately misleading note.

The same passage and instruction schema are used under each condition. Answers include a categorical label, free-text interpretation, an exact quote from the passage, whether context was used, an alternative interpretation, and confidence between zero and one.

The implemented baseline contains **40 fictional constructed fixtures in 10 motif families**, created for software tests. These should not be reported as authentic culturally situated passages. The test double selects a label using hardcoded probabilities; performance differences in its output are entirely artificial.

## Evaluation definitions

- **Agreement with constructed primary label:** useful as a pipeline check, not a validated accuracy measure.
- **Evidence presence:** whether the quoted span occurs verbatim in the passage; does not verify that the quote actually supports the proposed interpretation.
- **Alternative present:** whether the response supplies any nonempty alternative interpretation.
- **Overconfident error:** label mismatch at confidence at least 0.8.
- **Brier score:** squared confidence-versus-binary-agreement difference, which is not a fully calibrated multiclass measurement.
- **Paired differences:** mean label-agreement difference between a retrieval condition and passage-only on matching cases.
- **Clustered bootstrap:** resamples 10 motif families rather than treating all 40 variants as independent. This is illustrative only for the synthetic fixtures.

## Empirical study requirements before research claims

The next phase requires 30–50 licensed or public-domain source passages, demonstrable cultural and historical provenance, a precisely defined unit of evaluation and citation-backed retrieval packets. Annotators should represent appropriate contextual expertise, work independently, have a written protocol, disclose disagreement, and adjudicate difficult cases. Multiple valid readings should be captured rather than force-fit into one class.

Models should be evaluated with fixed prompts, parameters and documented model versions. A fair comparison needs balanced randomization of condition order, a full log of failures, duplicate checks, and a rubric sensitive to nuanced literary interpretations, cultural stereotyping, conflicting contextual evidence, and unsupported certainty.

## Scientific limitations

No actual LLM evaluation or human validation is claimed by the baseline. No causal inference about real retrieval methods follows from these contrived context packets. Prompts and labels may bias output toward a constructed answer. For claims of retrieval helpfulness, the retrieved evidence itself should be verified independently and the retrieval system characterized explicitly (index, ranking, source corpus, context size, contamination risk).

## Security and ethics

Do not store API keys or participant information in the repository. Public examples require clear copyright and licensing provenance. Cultural expertise and conflicting interpretations should be treated as substantive evidence, not automatically graded as incorrect.

## Reproducibility

Use Python 3.10+ with no external runtime dependencies. Execute `python -m unittest discover -s tests -v`, then `python -m culturaeval --backend demo --output results/demo`. For real LLM calls, the user must explicitly opt into the `api` backend and supply a suitable key and model. API results should be separated from deterministic demos.

## Research statement

This is a methodological prototype intended to facilitate future empirical research. It is **not** itself a research paper with validated results.
