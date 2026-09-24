"""Screenshot → Action Core."""

from .analyzer import analyze_text
from .schema import Action, ActionResult

__all__ = ["Action", "ActionResult", "analyze_text"]
__version__ = "0.2.1"
