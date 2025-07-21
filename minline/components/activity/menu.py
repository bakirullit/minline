from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from minline.runtime.language_manager import LanguageManager

class Menu:
    def __init__(self, menu_id = None, controls: list = None, text_id: str = None, lang: str = "en"):
        self.menu_id = menu_id  # will be set later by app
        self.text_id = text_id  # fallback to menu_id if None
        self.lang = lang
        self.controls = controls

    async def render(self, chat_id, message_id, bot, lang="en") -> tuple[str, InlineKeyboardMarkup, int | None]:
        title = LanguageManager.get(lang, self.text_id or self.menu_id)

        normalized_controls = []
        for row in self.controls:
            if isinstance(row, list):
                normalized_controls.append(row)
            else:
                normalized_controls.append([row])  # single button case

        normalized_controls = []
        for row in self.controls:
            if isinstance(row, list):
                normalized_controls.append(row)
            else:
                normalized_controls.append([row])  # single button case

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LanguageManager.get(lang, button.text_id),
                    callback_data=f"{self.lang}:{self.menu_id}:{button.action}"
                )
                for button in row
            ]
            for row in normalized_controls
        ])

        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=title,
                reply_markup=keyboard
            )
            return title, keyboard, message_id
        except Exception as E:
            sent: Message = await bot.send_message(
                chat_id=chat_id,
                text=title,
                reply_markup=keyboard
            )
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            return sent.text, sent.reply_markup, sent.message_id
