from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
import asyncio
import inspect
from .session.redis_manager import RedisSessionManager
from .runtime.language_manager import LanguageManager
from .runtime.renderer import render_menu

class MinlineApp:
    def __init__(self, token: str, *, language_dir: str = "languages", default_lang: str = "en"):
        self.token = token
        self.dp = Dispatcher(storage=MemoryStorage())
        self.bot = Bot(token=self.token)
        self.router = Router()
        self.menu_registry = {}
        self.default_lang = default_lang
        self.callback_handlers = {}

        self.lang = LanguageManager(language_dir)
        self.session = RedisSessionManager()

        # Register core handlers
        self.router.message(CommandStart())(self._start_handler)
        self.router.message()(self._delete_unknown)

        self.dp.include_router(self.router)

    def callback(self, key: str):
        def decorator(func):
            self.callback_handlers[key] = func
            return func
        return decorator
    
    def menu(self, menu_id: str):
        def wrapper(fn):
            self.menu_registry[menu_id] = fn
            return fn
        return wrapper

    async def _start_handler(self, message: Message):
        await message.delete()
        user_id = message.from_user.id
        chat_id = message.chat.id
        lang = self.default_lang

        menu = self.menu_registry.get("main_menu", lambda: None)()
        if not menu:
            await self.bot.send_message(chat_id, "Menu 'main_menu' not found.")
            return

        rendered = render_menu(menu, lang_code=lang)
        sent = await self.bot.send_message(chat_id, rendered.text, reply_markup=rendered.keyboard)

        await self.session.set_state(user_id, {
            "chat_id": chat_id,
            "message_id": sent.message_id,
            "lang": lang,
            "menu_id": "main_menu"
        })
    
        
    def _register_callbacks(self):
        @self.router.callback_query()
        async def _callback_handler(callback: CallbackQuery, bot: Bot):
            try:
                key = callback.data
                handler = self.callback_handlers.get(key)

                if handler:
                    sig = inspect.signature(handler)
                    param_count = len(sig.parameters)

                    if param_count == 2:
                        await handler(callback, {"bot": bot})
                    elif param_count == 1:
                        await handler(callback)
                    elif param_count == 0:
                        await handler()
                    else:
                        print(f"Unsupported handler signature for: {key}")
                else:
                    await callback.answer("No handler registered.", show_alert=True)

            except Exception as e:
                print("Callback error:", e)

    
    async def _delete_unknown(self, message: Message):
        await message.delete()

    def run(self):
        self._register_callbacks()
        asyncio.run(self.dp.start_polling(self.bot))

        @self.router.callback_query()
        async def _callback_handler(callback: CallbackQuery, bot: Bot):
            try:
                key = callback.data  # like "main_menu:open_settings"
                handler = self.callback_handlers.get(key)
                if handler:
                    await handler(callback, {"bot": bot})
                else:
                    await callback.answer("No handler registered.", show_alert=True)
            except Exception as e:
                print("Callback error:", e)

