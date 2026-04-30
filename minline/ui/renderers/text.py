"""Text question renderer - free-form user input."""

from minline.ui.renderers.base import BaseRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TextRenderer(BaseRenderer):
    """Renders text questions - no buttons, just free input."""
    
    def render(self, question, show_back: bool = False) -> InlineKeyboardMarkup | None:
        """Text questions have no buttons - user types freely."""
        if show_back:
            markup = InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="🔙 Back", callback_data="__back")
                ]]
            )
            return markup
        return None
    
    def parse_input(self, input_event) -> str:
        """Text input - return value as-is."""
        return str(input_event.value)
