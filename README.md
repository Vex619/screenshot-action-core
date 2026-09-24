# Screenshot → Action Core

**Turn screenshots into structured information and actionable next steps.**

Screenshot → Action Core is a small, privacy-conscious Python toolkit for extracting useful structure from screenshots such as assignments, events, receipts, flights, job posts, recipes, addresses, and messages.

> **Screenshot anything. Know what to do next.**

## Why this exists

Screenshots are an unstructured inbox. The useful information is usually a deadline, amount, place, contact, event, or next action. This project provides a deterministic, testable pipeline that turns extracted text into a normalized action-oriented result.

## Quick start

```bash
pip install -e .

screenshot-action text "Assignment due Friday at 11:59 PM"
screenshot-action text "Flight AI 102 departs Chennai at 18:30 on October 2"
screenshot-action text "Buy 2 items for ₹1,499"
```

The CLI emits JSON by default, making the output easy to pipe into other tools.

## Example

Input:

```text
Assignment 3 — submit by Friday 11:59 PM
```

Output:

```json
{
  "type": "assignment",
  "confidence": 0.92,
  "title": "Assignment 3",
  "entities": {
    "deadline": "Friday 11:59 PM"
  },
  "actions": [
    {
      "type": "create_task",
      "label": "Complete Assignment 3"
    },
    {
      "type": "set_reminder",
      "label": "Remind me before the deadline"
    }
  ]
}
```

## Architecture

```text
Image / text
    │
    ▼
Extraction layer ── optional OCR adapter
    │
    ▼
Normalization
    │
    ▼
Intent + entity detection
    │
    ▼
Action planner
    │
    ▼
Stable JSON schema
```

The core package intentionally keeps extraction and reasoning separate. That makes it possible to plug in Tesseract, a local vision model, or a hosted multimodal model without changing the downstream schema.

## Supported categories

The initial rules recognize common signals for:

- assignments / tasks
- events / appointments
- travel / flights
- receipts / purchases
- jobs / applications
- recipes
- addresses / locations
- generic reminders

This is a foundation, not a claim that every screenshot can be perfectly understood.

## Design principles

- **Local-first:** the core text pipeline has no network dependency.
- **Provider-agnostic:** OCR and vision models are adapters, not hard-coded requirements.
- **Structured output:** downstream automations consume a stable schema rather than free-form prose.
- **Human-in-the-loop:** actions are proposed, not silently executed.
- **Testable:** classification and extraction logic are deterministic and unit-tested.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Roadmap

- [x] Stable action schema
- [x] CLI text analyzer
- [x] Deterministic intent/entity extraction
- [x] Unit tests and CI
- [ ] OCR adapter
- [ ] FastAPI service
- [ ] Vision-model adapter interface
- [ ] Evaluation dataset and benchmark harness
- [ ] Calendar / task integrations as opt-in adapters

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please keep provider-specific code behind adapters and add tests for new extraction behavior.

## Security

Please see [SECURITY.md](SECURITY.md) for vulnerability reporting. Do not commit screenshots containing credentials, financial account numbers, authentication codes, or other sensitive information.

## License

MIT. See [LICENSE](LICENSE).
