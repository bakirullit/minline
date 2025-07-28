from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from minline.runtime.language_manager import LanguageManager
from .activity import Activity

class Input(Activity):
    def __init__(
        self,
        input_id: str,
        filter: str = "text",
        back_route: str = "//",
        save_to: str | None = None,
        text_id: str | None = None,
        lang: str = "en"
    ):
        super().__init__(menu_id=None, lang=lang)
        self.input_id = input_id
        self.filter = filter
        self.back_route = back_route
        self.save_to = save_to
        self.text_id = text_id or input_id



    async def render(self, chat_id, message_id, bot, lang="en") -> tuple[str, InlineKeyboardMarkup, int | None]:
        title = LanguageManager.get(lang, self.text_id or self.menu_id)
        try:
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="← Back", callback_data=f"{lang}:Input-{self.input_id}:#route://")]
            ])

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
                reply_markup=None
            )
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            return sent.text, sent.reply_markup, sent.message_id
