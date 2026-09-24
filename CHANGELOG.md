# Changelog

All notable changes to this project will be documented here.

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
