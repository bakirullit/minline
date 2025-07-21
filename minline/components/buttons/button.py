from aiogram.types import InlineKeyboardButton

class Button:
    def __init__(self, text_id: str, action: str, data: dict = None):
        self.text_id = text_id
        self.action = action
        self.data = data or {}
