# Changelog

All notable changes to this project will be documented here.

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
