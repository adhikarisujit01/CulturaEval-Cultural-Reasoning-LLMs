# Source-based authentic-text pilot

This pilot differs from the synthetic test runner. It preserves raw answers under all four conditions and **does not calculate culturally valid accuracy** without human review.

## Prerequisites

- Python 3.10+
- Authenticated OpenAI API key in the current shell, named `CULTURAEVAL_API_KEY`
- API billing and model access; calls may incur charges

## Run

```bash
git pull
python3 -m culturaeval.authentic_pilot --model gpt-4.1-mini --limit 2 --output results/authentic-pilot/gpt-4.1-mini
```

Expect **8 API requests** if all work. Read `report.json` for failures; inspect `model_responses.jsonl` for original answers and usage.

If testing a second model:

```bash
python3 -m culturaeval.authentic_pilot --model gpt-4.1 --limit 2 --output results/authentic-pilot/gpt-4.1
```

The older `python3 -m culturaeval` default dataset is entirely synthetic and its label accuracy must **not** be reported as empirical cultural reasoning ability.

### Dataset provenance

- `AUTH-PILOT-GITA-01`: *Bhagavad Gita*, Chapter II, poetic English translation by Edwin Arnold, Project Gutenberg #2388. https://www.gutenberg.org/cache/epub/2388/pg2388-images.html
- `AUTH-PILOT-RAMA-01`: *Ramayana*, Aranya Kanda, Section XLIII, English translation by Manmatha Nath Dutt, Project Gutenberg #57826. https://www.gutenberg.org/files/57826/57826-h/57826-h.html

Exact short passage excerpts were checked against the linked online translations. Context notes are provisional summaries of the surrounding passages. The misleading notes are deliberately false interventions, **not sourced claims**. Pilot not ready for benchmark publication, model comparison conclusions, or scholarly conclusions without source expansion and independent human annotations.

### Human-review next step

For each model response, independently rate cultural reasoning and interpretive plurality on the separate 0–4 scales in `docs/dual-axis-evaluation.md`. Record disputed interpretations and source-linked evidence; do not treat repeated model responses or author-only notes as independent validation. Consider translation effects and biases introduced by using English verse versions.
