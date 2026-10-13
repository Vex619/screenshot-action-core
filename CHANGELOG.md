# Changelog

All notable changes to this project will be documented here.

## [0.2.2] - 2026-10-13

### Fixed

- Dates such as `2026-10-02` were also reported as a `phone` entity.
- Ordinary words ending in "st"/"rd"/"ln" ("must", "first", "word") produced false `address`
  entities, and an address match could swallow the rest of the text.
- Keywords were matched as raw substrings, so "Baker Street" was classified as a recipe
  ("bake") and words like "taxi" or "investigate" triggered `receipt` / `travel`. Keywords now
  match whole words (plurals allowed); "overdue" was added to the assignment terms.
- `tonight` normalized to tomorrow's date instead of the reference date.
- Amounts were matched inside words ("hours 9" -> `rs 9`) and kept a trailing comma ("$5,").
- Titles lost their first word(s) ("Assignment 3 — ..." became "3 — ..."), and multi-line input
  produced one long run-on title. Titles now use the first line; a leading label such as
  "Assignment:" is only removed when followed by a separator.
- URLs kept a trailing sentence period or comma.
- AM/PM markers could be reported as a flight number.
- `POST /analyze/text` returned HTTP 500 for blank text; it now returns 422.
- `metadata.version`, the API version and the package version could disagree; the version now
  lives only in `src/screenshot_action/_version.py`.
- README shell examples used `\\` line continuations that do not work in a shell, and the
  sample output did not match the real CLI output.
- CLI exited with an encoding error when stdout could not encode `₹` or `—` (legacy Windows
  code pages); it now falls back to escaped JSON.
- `scripts_evaluate.py` only worked when run from the repository root.
- The OCR adapter left the image file open.

### Changed

- `source_text` now keeps line breaks (whitespace inside each line is still collapsed).
- The event reminder label reads "Set a reminder before the event".

### Added

- `screenshot-action --version`, and `main(argv)` for in-process CLI testing.
- Regression tests for every fix above, evaluation cases as pytest tests, and a check that
  `examples/assignment.json` matches real analyzer output.
- Release workflow now runs tests and lint before publishing.
- `pythonpath = ["src"]` for pytest, Python 3.10-3.14 classifiers and project URLs.

## [0.2.1] - 2026-09-24

### Improved

- CI now validates Python 3.10 through 3.14.
- CI installs and tests the optional API stack instead of skipping the API test.
- CI runs the synthetic evaluation harness and package build.
- Release publishing is automated from version tags.
- Added the `py.typed` marker for downstream type checkers.

## [0.2.0] - 2026-09-24

### Added

- Relative and absolute date normalization with an optional reference date.
- Extraction of URLs, email addresses, phone-like strings, and richer metadata.
- Action payloads that carry normalized date/time context when available.
- Optional FastAPI service with health and text-analysis endpoints.
- Synthetic regression dataset and dependency-free evaluation harness.
- Docker image definition and Make targets for common developer tasks.
- Expanded tests covering the analyzer, CLI, and API.

## [0.1.0] - 2026-09-24

### Added

- Stable `ActionResult` and `Action` schemas.
- Deterministic classification for common screenshot categories.
- Entity extraction for dates, times, amounts, and flight identifiers.
- CLI for text, file, and local OCR analysis.
- Initial unit test suite and developer tooling.
