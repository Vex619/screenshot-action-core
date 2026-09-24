"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .analyzer import analyze_text


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="screenshot-action",
        description="Turn screenshot content into structured actions.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(command: argparse.ArgumentParser) -> None:
        command.add_argument("--reference-date", help="Reference date (YYYY-MM-DD) for relative dates")
        command.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    text = sub.add_parser("text", help="Analyze already-extracted text")
    text.add_argument("value", help="Text to analyze")
    add_common(text)

    file_cmd = sub.add_parser("file", help="Analyze text stored in a file")
    file_cmd.add_argument("path", type=Path)
    add_common(file_cmd)

    image_cmd = sub.add_parser("image", help="OCR an image locally, then analyze it")
    image_cmd.add_argument("path", type=Path)
    add_common(image_cmd)
    return parser


def _reference_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("--reference-date must use YYYY-MM-DD") from exc


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "text":
            text = args.value
        elif args.command == "file":
            text = args.path.read_text(encoding="utf-8")
        else:
            from .ocr import extract_text_from_image
            text = extract_text_from_image(args.path)

        result = analyze_text(text, reference_date=_reference_date(args.reference_date)).to_dict()
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 0
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
