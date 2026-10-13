"""Screenshot → Action Core."""

from ._version import __version__
from .analyzer import analyze_text
from .schema import Action, ActionResult

__all__ = ["Action", "ActionResult", "__version__", "analyze_text"]
