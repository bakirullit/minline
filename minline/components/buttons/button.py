from aiogram.types import InlineKeyboardButton

class Button:
    def __init__(self, text_id: str, action: str):
        self.text_id = text_id
        self.action = action

    def build(self, menu_id: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=f"{menu_id}:{self.action}"
        )
