"""Multi choice question renderer - toggle buttons with submit."""

from minline.ui.renderers.base import BaseRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class MultiChoiceRenderer(BaseRenderer):
    """Renders multi choice - toggle buttons (✓/☐) + submit button."""
    
    def render(self, question, show_back: bool = False) -> InlineKeyboardMarkup:
        """Render items as toggle buttons + submit."""
        items = question.config.get("items", [])
        selected = question.config.get("selected", set())
        
        buttons = []
        for idx, item in enumerate(items):
            prefix = "✅" if idx in selected else "☐"
            buttons.append([
                InlineKeyboardButton(
                    text=f"{prefix} {item}",
                    callback_data=f"__toggle_{idx}"
                )
            ])
        
        # Submit button
        buttons.append([InlineKeyboardButton(text="✓ Done", callback_data="__submit")])
        
        if show_back:
            buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="__back")])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def parse_input(self, input_event) -> list:
        """Parse multi choice input - return list of selected indices."""
        if input_event.type == "callback":
            # Extract selected indices from callback
            if input_event.value.startswith("__toggle_"):
                idx = int(input_event.value.split("_")[-1])
                return [idx]  # Toggle logic handled in session
        raise TypeError(f"Unsupported input for multi_choice: {input_event.type}")
