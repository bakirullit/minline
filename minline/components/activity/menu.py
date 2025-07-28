from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from minline.runtime.language_manager import LanguageManager
from .activity import Activity

class Menu(Activity):
    def __init__(self, menu_id: str = None, controls: list = None, text_id: str = None, lang: str = "en"):
        super().__init__(menu_id=menu_id, lang=lang)
        self.text_id = text_id or menu_id
        self.controls = controls or []

    async def render(self, chat_id, message_id, bot, lang="en") -> tuple[str, InlineKeyboardMarkup, int | None]:
        title = LanguageManager.get(lang, self.text_id or self.menu_id)

        normalized_controls = []
        for row in self.controls:
            if isinstance(row, list):
                normalized_controls.append(row)
            else:
                normalized_controls.append([row])  # single buttonWebAppInfo case

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
                    callback_data=None if button.url or button.web_app_url else f"{lang}:{self.menu_id}:{button.action}",
                    url=button.url,
                    web_app=WebAppInfo(url=button.web_app_url) if button.web_app_url else None
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
