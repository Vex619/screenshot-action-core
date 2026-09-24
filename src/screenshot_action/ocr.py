"""Optional local OCR adapter.

Install with `pip install -e '.[ocr]'`. Tesseract itself must also be installed
on the host. This module is deliberately optional so the core package stays
provider-agnostic and network-free.
"""

from __future__ import annotations

from pathlib import Path


def extract_text_from_image(path: str | Path) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("OCR support requires the 'ocr' extra: pip install -e '.[ocr]'") from exc

    image_path = Path(path)
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    return pytesseract.image_to_string(Image.open(image_path)).strip()
