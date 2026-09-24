# Evaluation harness

The repository includes a small synthetic regression set under `evaluation/cases.jsonl`.
It intentionally contains no real personal data.

Run it with:

```bash
python scripts_evaluate.py
```

Each case checks the predicted category and a set of expected entity keys. The harness is
designed to stay deterministic so changes to extraction logic can be reviewed as ordinary
code changes.

The dataset is not a benchmark of general multimodal intelligence. It is a project-level
regression suite for the deterministic analyzer.
