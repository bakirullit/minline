"""Single choice question renderer - numbered options."""

from minline.ui.renderers.base import BaseRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class SingleChoiceRenderer(BaseRenderer):
    """Renders single choice - each option as numbered button (1, 2, 3, ...)."""
    
    def render(self, question, show_back: bool = False) -> InlineKeyboardMarkup:
        """Render items as numbered buttons."""
        items = question.config.get("items", [])
        
        buttons = []
        for idx, item in enumerate(items, 1):
            buttons.append([
                InlineKeyboardButton(text=f"{idx} {item}", callback_data=f"__choice_{idx-1}")
            ])
        
        if show_back:
            buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="__back")])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def parse_input(self, input_event) -> str:
        """Parse numeric input (1, 2, 3) to item index."""
        if input_event.type == "number":
            return input_event.value
        if input_event.type == "text":
            try:
                return int(input_event.value)
            except ValueError:
                raise ValueError(f"Expected number, got: {input_event.value}")
        raise TypeError(f"Unsupported input type for single_choice: {input_event.type}")
