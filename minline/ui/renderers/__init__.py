"""Question renderer abstraction - pluggable UI generation."""

from minline.ui.renderers.base import BaseRenderer
from minline.ui.renderers.text import TextRenderer
from minline.ui.renderers.single_choice import SingleChoiceRenderer
from minline.ui.renderers.multi_choice import MultiChoiceRenderer
from minline.ui.renderers.date_picker import DatePickerRenderer

# Global renderer registry
RENDERERS = {
    "text": TextRenderer(),
    "single_choice": SingleChoiceRenderer(),
    "multi_choice": MultiChoiceRenderer(),
    "date_picker": DatePickerRenderer(),
}


def get_renderer(name: str) -> BaseRenderer:
    """Get renderer by name."""
    if name not in RENDERERS:
        raise ValueError(f"Unknown renderer: {name}. Available: {list(RENDERERS.keys())}")
    return RENDERERS[name]


def register_renderer(name: str, renderer: BaseRenderer):
    """Register custom renderer."""
    RENDERERS[name] = renderer


__all__ = ["get_renderer", "register_renderer", "BaseRenderer"]
