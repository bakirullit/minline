from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..components.buttons.button import Button 
from ..components.activity.menu import Menu
from .language_manager import LanguageManager

class RenderedMenu:
    def __init__(self, text: str, keyboard: InlineKeyboardMarkup):
        self.text = text
        self.keyboard = keyboard

def render_menu(menu: Menu, lang_code: str = "en") -> RenderedMenu:
    rows = []
    for row in menu.controls:
        button_row = []
        for control in row:
            if isinstance(control, Button):
                text = LanguageManager.get(lang_code, control.text_id)
                callback_data = f"{menu.menu_id}:{control.action}"
                button_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
            # You can extend this for ToggleButton, LinkButton, etc.
        rows.append(button_row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    text = LanguageManager.get(lang_code, menu.text_id or menu.menu_id)
    return RenderedMenu(text=text, keyboard=keyboard)
