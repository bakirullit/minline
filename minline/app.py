# Minline - Custom Telegram Menu Framework
# Copyright (c) 2025 Bakirullit
# License: Minline License (Non-Commercial) – see LICENSE file for details

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from typing import Callable, Awaitable
from .session.redis_manager import RedisSessionManager
from .runtime.language_manager import LanguageManager
from .components.buttons.button import Button  # assuming your Menu and Button classes are here
from .components.activity.menu import Menu

class MinlineApp:
    def __init__(self, token: str, *, language_dir: str = "languages", default_lang: str = "en"):
        self.token = token
        self.dp = Dispatcher(storage=MemoryStorage())
        self.bot = Bot(token=self.token)
        self.router = Router()
        self.default_lang = default_lang
        self.menu_registry = {}
        self.action_commands: dict[str, Callable[[CallbackQuery, str], Awaitable]] = {}
        self.lang = LanguageManager(language_dir)
        self.session = RedisSessionManager()
        self.router.message(CommandStart())(self._menu_handler)
        self.router.message()(self._delete_unknown)
        self._register_callbacks() 
        self.dp.include_router(self.router)

    def action(self, name: str):
        def decorator(func):
            self.action_commands[name] = func
            return func
        return decorator

    def menu(self, path: str):
        def decorator(fn):
            menu_instance = fn()
            menu_instance.menu_id = path
            if path != "/":
                back_button = Button("back", f"#route://")
                menu_instance.controls.insert(0, [back_button])
            self.menu_registry[path] = menu_instance
            return menu_instance
        return decorator

    async def _menu_handler(self, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        lang = self.default_lang
        state = await self.session.get_state(user_id)
        if state:
            old_chat_id = state.get("chat_id")
            old_message_id = state.get("message_id")
            if old_chat_id and old_message_id:
                try:
                    await self.bot.delete_message(old_chat_id, old_message_id)
                except Exception:
                    pass
        menu = self.menu_registry.get("/")
        if not menu:
            await self.bot.send_message(chat_id, "Menu '/' not found.")
            return
        _, _, message_id = await menu.render(chat_id, None, self.bot, lang)
        await self.session.set_state(user_id, {
            "chat_id": chat_id,
            "message_id": message_id,
            "lang": lang,
            "menu_path": "/"
        })

        try:
            await message.delete()
        except Exception:
            pass

    def _register_callbacks(self):
        @self.router.callback_query()
        async def callback_handler(callback: CallbackQuery):
            user_id = callback.from_user.id
            data = callback.data
            if not data or ":" not in data:
                return
            
            parts = data.split(":", maxsplit=3)
            if len(parts) < 3:
                return
            
            lang, current_path, command = parts[0], parts[1], parts[2]
            arg = parts[3] if len(parts) > 3 else ""
            print(f"Callback received: lang={lang}, path={current_path}, command={command}, arg={arg}", parts)

            if not command.startswith("#"):
                return

            if (command == "#route"):
                state = await self.session.get_state(user_id)
                if not state:
                    return

                chat_id = state["chat_id"]
                message_id = state["message_id"]

                if arg == "//":
                    path_parts = current_path.rstrip("/").split("/")
                    new_path = "/" if len(path_parts) <= 2 else "/".join(path_parts[:-1])
                else:
                    new_path = current_path.rstrip("/") + "/" + arg
                menu = self.menu_registry.get(new_path)
                if not menu:
                    await callback.answer("Menu not found", show_alert=True)
                    return

                _, _, new_msg_id = await menu.render(chat_id, message_id, self.bot, lang)
                await self.session.set_state(user_id, {
                    "chat_id": chat_id,
                    "message_id": new_msg_id,
                    "lang": lang,
                    "menu_path": new_path
                })

                await callback.answer()
                return

            if command in self.action_commands:
                await self.action_commands[command](callback, command)
                return

            await callback.answer("Unknown action", show_alert=True)

    async def _open_menu(self, user_id: int, menu: Menu, path: str):
        state = await self.session.get_state(user_id)
        if not state:
            return

        chat_id = state["chat_id"]
        message_id = state["message_id"]
        lang = state.get("lang", self.default_lang)
        menu.lang = lang
        await menu.render(chat_id, message_id, self.bot)

        state["menu_path"] = path
        await self.session.set_state(user_id, state)

    async def _delete_unknown(self, message: Message):
        await message.delete()

    def run(self):
        asyncio.run(self.dp.start_polling(self.bot))
        
