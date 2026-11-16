# CulturaEval
## Cultural Context as Evidence: When Retrieval Helps and Hurts LLM Interpretation

**Author:** Sujit Adhikari  
**Status:** Working research prototype; *not* a peer-reviewed paper or validated empirical study.

**Research question:** Under what conditions does retrieved cultural and historical knowledge improve or degrade language-model interpretation of culturally situated texts?

CulturaEval is a reproducible experimental scaffold comparing the interpretation of the same passage with four evidence conditions.

| Condition | Context supplied |
|---|---|
| `passage_only` | No external evidence |
| `relevant` | Context constructed to clarify the passage |
| `partial` | Accurate but incomplete contextual note |
| `misleading` | Plausible but deliberately incorrect note |

The generic synthetic framework and source-based pilot use different response schemas. The source-based pilot records a main interpretation, passage evidence, mentioned context claims, alternatives, uncertainty and likely errors.

### Quick start

Python 3.10+ (standard library only):

```bash
python -m unittest discover -s tests -v
python -m culturaeval --backend demo --output results/demo
```

This generates a synthetic-data **infrastructure smoke test**, **not research results**. The demonstration backend is deterministic and does not call a language model.

#### Optional real LLM evaluation

```bash
export CULTURAEVAL_API_KEY='YOUR_KEY'
python -m culturaeval --backend api --model YOUR_MODEL --limit 4 --output results/real-model
```

The optional API backend uses an OpenAI-compatible Chat Completions JSON response; it may incur usage charges and requires an explicit opt-in. Do not commit credentials.

### Source-based exploratory pilot (executed; limited human review)

A separate, source-linked pilot runner has been executed under two prompt protocols, each with eight successful calls to GPT-4.1 mini. It evaluates **two short excerpts** from historical English translations of the *Bhagavad Gita* and *Ramayana*. The four evidence conditions save raw model responses and request metadata. Results are stored locally and are not committed by default.

```bash
export CULTURAEVAL_API_KEY='YOUR_KEY'
python -m culturaeval.authentic_pilot --model gpt-4.1-mini --limit 2 --output results/authentic-pilot-v2/gpt-4.1-mini
```

With two cases and four conditions, each execution makes up to **eight paid API requests**. It is **not automatically run** by the test suite. See [pilot instructions](docs/authentic-pilot.md), [source register](docs/authentic-source-register.md), and [dual-axis human evaluation rubric](docs/dual-axis-evaluation.md).

The primary evaluation distinguishes **culturally grounded interpretation** from **recognition of multiple defensible interpretations**. These are human-scored dimensions (0–4 each), not automated accuracy values. Two reviewers have now rated **only the two misleading-context responses** from the condition-masked GPT-4.1-mini pilot. These are limited preliminary judgments, not expert validation or a benchmark-level performance result. The remaining responses lack human ratings. See [limited human review](docs/limited-human-review.md), [anonymized scores](docs/human-review-scores.csv), and [exploratory case study](docs/exploratory-case-study.md).

### Current experimental evidence

- **Experiment 1:** eight completed API requests with the original prompt protocol; no human ratings.
- **Experiment 2:** eight completed API requests with condition labels and explicit adversarial warnings removed from the model-facing prompt; no API failures reported.
- **Human ratings:** two independent invited reviewers assessed only the Gita and Ramayana **misleading-context** responses from Experiment 2, yielding four reviewer–passage rating rows. Reviewers disagreed on the two main axes; this disagreement is reported without adjudication.
- **Interpretive finding:** a possible secondary-reasoning contamination pattern in the Ramayana response, where false supplied context appears in subsequent explanation despite a broadly plausible main interpretation. This remains a small exploratory case observation, not a reliable prevalence or causal estimate.

See [the reviewed-results report](docs/limited-human-review.md), [reviewer scores](docs/human-review-scores.csv), and [preliminary source-evidence audit](docs/preliminary-source-evidence-audit.md).

### Contents

- `culturaeval/`: prompt construction, response validation, metrics, synthetic demo, and optional API runner.
- `data/synthetic_cases.jsonl`: 40 **fictional** test fixtures (10 motifs × 4 variants), not independently annotated literary evidence.
- `data/authentic_pilot_candidates.jsonl`: two source-linked historical-translation pilot cases, awaiting independent validation.
- `tests/`: unit and integration tests.
- `docs/methodology.md`: experimental plan, research caveats, and next milestones.
- `docs/annotation-guide.md`: proposed manual annotation protocol.

### Important limitations

The constructed passages and labels are not culturally authenticated. The repeated variants are **not 40 independent observations**. Exact quoted spans show only that a quote is present, not that an interpretation is correct. The synthetic demo cannot establish that retrieval helps or harms real language models. A credible empirical paper requires licensed literary samples, documented retrieval provenance, independent annotations, actual model responses, and statistical evaluation.

### Research direction

The next phase will curate 30–50 culturally situated source passages with legal reuse permissions, source-check context packets, involve multiple annotators, and compare model behavior across conditions while reporting uncertainty and disagreement.

### Attribution

This is a new research portfolio project, distinct from the author's earlier coursework. Code-development assistance may include AI tools. Authorship, data provenance and research milestones should be represented accurately.

**License:** Code MIT; constructed benchmark fixtures CC0-1.0.
