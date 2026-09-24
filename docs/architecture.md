# Architecture

Screenshot → Action Core separates four concerns:

1. **Extraction** — turn an image or other source into text. The initial optional adapter uses local Tesseract OCR.
2. **Analysis** — classify the content and extract lightweight entities.
3. **Action planning** — propose safe, descriptive next steps.
4. **Integration** — future adapters can send approved actions to calendars, task managers, maps, or other systems.

The core analyzer has no network calls and never executes an action. This boundary is intentional: integrations should be explicit and user-controlled.

## Extension point

A vision-model adapter should ultimately return normalized text plus optional model metadata. It should not bypass `ActionResult` or directly invoke external actions.
