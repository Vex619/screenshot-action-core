"""Optional FastAPI service for Screenshot → Action Core."""

from __future__ import annotations

from datetime import date

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - optional dependency
    FastAPI = None  # type: ignore[assignment,misc]
    BaseModel = object  # type: ignore[assignment,misc]


if BaseModel is not object:

    class TextRequest(BaseModel):
        text: str
        reference_date: date | None = None


    def create_app():
        """Create the FastAPI application."""
        from .analyzer import analyze_text

        app = FastAPI(title="Screenshot → Action Core", version="0.2.0")

        @app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok", "version": "0.2.0"}

        @app.post("/analyze/text")
        def analyze(payload: TextRequest) -> dict:
            return analyze_text(
                payload.text,
                reference_date=payload.reference_date,
            ).to_dict()

        return app


    app = create_app()
else:

    def create_app():
        raise RuntimeError("API support requires the 'api' extra")

    app = None
