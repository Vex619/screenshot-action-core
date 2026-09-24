# Architecture

Screenshot → Action Core separates four concerns:

1. **Extraction** — convert an image or other source into text. The initial optional adapter uses local Tesseract OCR.
2. **Analysis** — classify the content and extract lightweight entities.
3. **Action planning** — propose safe, descriptive next steps.
4. **Integration** — future adapters can send approved actions to calendars, task managers, maps, or other systems.

## Core boundary

The analyzer has no network calls and never executes an action. `ActionResult` is the boundary
between analysis and integrations.

## Optional API

`src/screenshot_action/api.py` exposes a small FastAPI service when the `api` extra is installed.
The service currently provides:

- `GET /health`
- `POST /analyze/text`

Image upload and vision-model adapters remain separate concerns so the core package stays small
and dependency-free.

## Compatibility

New metadata and fields should be additive where practical. Breaking changes require a version
bump and a changelog entry.
