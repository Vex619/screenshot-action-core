# AGENTS.md

## Project goal

Build a provider-agnostic, testable pipeline that converts screenshot content into structured information and proposed actions.

## Engineering rules

- Preserve the stable public schema unless a breaking change is intentional and documented.
- Keep core logic deterministic and network-free.
- Put OCR, vision models, hosted APIs, and integrations behind explicit adapters.
- Never execute actions from the core analyzer.
- Add regression tests for extraction/classification behavior.
- Do not add real personal data or credentials to fixtures.
- Prefer small, composable modules over a monolithic analyzer.

## Validation

Run:

```bash
pytest
ruff check .
```

Before a release, verify the CLI and update `CHANGELOG.md`.
