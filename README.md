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

Responses contain an interpretation label, short explanation, exact passage quote, a context-use flag, an alternative interpretation and a confidence score.

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

### Contents

- `culturaeval/`: prompt construction, response validation, metrics, synthetic demo, and optional API runner.
- `data/synthetic_cases.jsonl`: 40 **fictional** test fixtures (10 motifs × 4 variants), not independently annotated literary evidence.
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
