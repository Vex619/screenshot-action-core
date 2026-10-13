"""Optional FastAPI service for Screenshot → Action Core."""

from __future__ import annotations

from datetime import date
from typing import Any

from ._version import __version__
from .analyzer import analyze_text

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - optional dependency
    FastAPI = None  # type: ignore[assignment,misc]
    HTTPException = None  # type: ignore[assignment,misc]
    BaseModel = object  # type: ignore[assignment,misc]


if BaseModel is not object:

    class TextRequest(BaseModel):
        text: str
        reference_date: date | None = None

    def create_app() -> FastAPI:
        """Create the FastAPI application."""
        app = FastAPI(title="Screenshot → Action Core", version=__version__)

        @app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok", "version": __version__}

        @app.post("/analyze/text")
        def analyze(payload: TextRequest) -> dict[str, Any]:
            try:
                result = analyze_text(payload.text, reference_date=payload.reference_date)
            except ValueError as exc:  # e.g. blank text: a client error, not a server crash
                raise HTTPException(status_code=422, detail=str(exc)) from exc
            return result.to_dict()

        return app

    app = create_app()
else:

    def create_app():  # type: ignore[no-untyped-def]
        raise RuntimeError("API support requires the 'api' extra")

    app = None
