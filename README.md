# Screenshot → Action Core

**Turn screenshots into structured information and actionable next steps.**

Screenshot → Action Core is a provider-agnostic Python toolkit for turning extracted screenshot
content into a stable JSON representation of **what the content is, what was found, and what could
be done next**.

> **Screenshot anything. Know what to do next.**

## What it does

The core pipeline is deliberately small:

```text
Image / text
     ↓
Extraction (optional OCR / vision adapter)
     ↓
Normalization
     ↓
Intent + entity detection
     ↓
Action planning
     ↓
Stable JSON
     ↓
Human approval / integration
```

Current deterministic categories include assignments, events, travel, receipts, jobs, recipes,
addresses, and generic reminders.

## Quick start

```bash
python -m pip install -e .

screenshot-action text "Assignment 3 — submit by Friday 11:59 PM" --pretty
```

Relative dates can be normalized with an explicit reference date:

```bash
screenshot-action text "Appointment tomorrow at 7 PM" \\
  --reference-date 2026-09-24 --pretty
```

Example output:

```json
{
  "type": "event",
  "confidence": 0.86,
  "title": "Appointment tomorrow at 7 PM",
  "entities": {
    "date": "tomorrow",
    "date_iso": "2026-09-25",
    "time": "7 PM"
  },
  "actions": [
    {
      "type": "create_task",
      "label": "Review Appointment tomorrow at 7 PM",
      "payload": {}
    },
    {
      "type": "set_reminder",
      "label": "Set a reminder before the deadline",
      "payload": {
        "date": "2026-09-25",
        "time": "7 PM"
      }
    }
  ]
}
```

## Image input

Local OCR is optional:

```bash
python -m pip install -e '.[ocr]'
screenshot-action image ./screenshot.png --pretty
```

The host also needs Tesseract installed. The OCR adapter is intentionally replaceable with a
vision-model adapter later.

## Python API

```python
from screenshot_action import analyze_text

result = analyze_text("Assignment due tomorrow at 8 PM")
print(result.to_dict())
```

## Optional API

```bash
python -m pip install -e '.[api]'
uvicorn screenshot_action.api:app --reload
```

Then:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/analyze/text \\
  -H 'content-type: application/json' \\
  -d '{"text":"Flight AI 102 departs tomorrow at 18:30","reference_date":"2026-09-24"}'
```

## Design principles

- **Local-first:** the core text pipeline has no network dependency.
- **Provider-agnostic:** OCR, vision models, and hosted APIs are adapters.
- **Structured output:** downstream systems consume a stable schema instead of free-form prose.
- **Human-in-the-loop:** the core proposes actions; it does not silently execute them.
- **Deterministic and testable:** extraction logic can be regression-tested without a model API.
- **Privacy-conscious:** fixtures are synthetic and the core does not upload screenshot content.

## Development

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts_evaluate.py
```

See [docs/architecture.md](docs/architecture.md) and [docs/evaluation.md](docs/evaluation.md).

## Project layout

```text
src/screenshot_action/     core library, CLI, OCR adapter, optional API
tests/                     regression tests
evaluation/                synthetic evaluation cases
docs/                      architecture + evaluation notes
.github/                   CI + issue/PR templates
```

## Roadmap

- [x] Stable action schema
- [x] Deterministic analyzer
- [x] CLI for text, file, and image input
- [x] Optional local OCR adapter
- [x] Relative/absolute date normalization
- [x] Optional FastAPI service
- [x] Synthetic evaluation harness
- [ ] Vision-model adapter interface
- [ ] Confidence calibration and provenance metadata
- [ ] Multimodal evaluation corpus
- [ ] Opt-in calendar/task/map integrations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep provider-specific integrations behind adapters and
add regression tests for behavior changes.

## Security

See [SECURITY.md](SECURITY.md). Never commit credentials, authentication codes, financial account
numbers, or private screenshots.

## License

MIT.
