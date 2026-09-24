"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import analyze_text


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="screenshot-action", description="Turn screenshot text into actions.")
    sub = parser.add_subparsers(dest="command", required=True)

    text = sub.add_parser("text", help="Analyze already-extracted text")
    text.add_argument("value", help="Text to analyze")
    text.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    file_cmd = sub.add_parser("file", help="Analyze text stored in a file")
    file_cmd.add_argument("path", type=Path)
    file_cmd.add_argument("--pretty", action="store_true")

    image_cmd = sub.add_parser("image", help="OCR an image locally, then analyze it")
    image_cmd.add_argument("path", type=Path)
    image_cmd.add_argument("--pretty", action="store_true")
    return parser


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
        result = analyze_text(text).to_dict()
        indent = 2 if args.pretty else None
        print(json.dumps(result, indent=indent, ensure_ascii=False))
        return 0
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
