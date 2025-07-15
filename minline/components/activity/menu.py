from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from minline.runtime.language_manager import LanguageManager

class Menu:
    def __init__(self, menu_id: str, controls: list = None, text_id: str = None, lang: str = "en"):
        self.menu_id = menu_id
        self.text_id = text_id or menu_id
        self.lang = lang
        self.controls = controls or []
        
    async def render(self, chat_id, message_id, bot):
        text_by_lang = LanguageManager.get(self.lang, "some_title_id")  # Assume you define it

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=LanguageManager.get(self.lang, button.text_id),
                callback_data=f"{self.menu_id}:{button.action}"
            )] for button in self.controls
        ])

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text_by_lang,
            reply_markup=keyboard
        )