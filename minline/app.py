from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from typing import Callable, Awaitable
from .session.session_manager import SQLiteSessionManager  # changed from Redis
from .runtime.language_manager import LanguageManager
from .components.buttons.button import Button
from .components.activity.menu import Menu
from .components.activity.input import Input

INPUT_FILTERS = {
    "text": lambda m: m.text is not None,
    "photo": lambda m: m.photo is not None,
    "document": lambda m: m.document is not None,
    "any": lambda m: True
}

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
        self.session = SQLiteSessionManager("local.db")  # updated
        self._input_handlers = {}
        self.dp.include_router(self.router)
        self.router.message(CommandStart())(self._menu_handler)
        self.router.message()(self._delete_unknown)
        self._register_callbacks()
        self._register_input_handler()

    async def startup(self):
        await self.session.init()  # added

    def action(self, name: str):
        def decorator(func):
            self.action_commands[name] = func
            return func
        return decorator

    def input(self, input_id: str, filter: str = "any"):
        def decorator(func):
            self._input_handlers[input_id] = {
                "handler": func,
                "filter": INPUT_FILTERS.get(filter, INPUT_FILTERS["any"])
            }
            return func
        return decorator

    def route(self, path: str):
        def decorator(fn):
            instance = fn()
            instance.menu_id = path

            if path != "/" and hasattr(instance, "controls"):
                back_button = Button("back", "#route://")
                instance.controls.insert(0, [back_button])

            if isinstance(instance, Input) and instance.back_route == "//":
                segments = path.strip("/").split("/")
                parent = "/" + "/".join(segments[:-1]) if len(segments) >= 1 else "/"
                instance.back_route = parent

            self.menu_registry[path] = instance
            print(f"Registering {path}")
            return instance
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

    async def process_input(self, message: Message):
        user_id = message.chat.id
        state = await self.session.get_state(user_id)
        if not state:
            return

        input_id = state.get("input_id")
        filter_id = state.get("filter")

        entry = self._input_handlers.get(input_id)
        if not entry:
            return

        if not INPUT_FILTERS.get(filter_id, lambda _: False)(message):
            await message.delete()
            return

        await self.session.delete_state(user_id)

        # Save file if requested
        activity = self.menu_registry.get(state.get("menu_path"))
        if isinstance(activity, Input) and activity.save_to:
            if message.photo:
                file_id = message.photo[-1].file_id
            elif message.document:
                file_id = message.document.file_id
            else:
                file_id = None

            if file_id:
                file = await self.bot.get_file(file_id)
                path = f"{activity.save_to}/{file.file_unique_id}"
                await self.bot.download_file(file.file_path, destination=path)

        await entry["handler"](message)


    def _register_input_handler(self):
        @self.router.message()
        async def universal_input_router(message: Message):
            await self.process_input(message)

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

            if command == "#route":
                state = await self.session.get_state(user_id)
                if not state:
                    return
                chat_id = state["chat_id"]
                message_id = state["message_id"]

                if arg == "//":
                    path_parts = current_path.rstrip("/").split("/")
                    new_path = "/" if len(path_parts) <= 2 else "/".join(path_parts[:-1])
                else:
                    new_path = (current_path.rstrip("/") + "/" + arg.lstrip("/")).replace("//", "/")

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
                if isinstance(menu, Input):
                    await self.set_input_state(user_id, menu.input_id, menu.filter)
                await callback.answer()
                return

            if command in self.action_commands:
                await self.action_commands[command](callback, command)
                return

            await callback.answer("Unknown action", show_alert=True)

    async def set_input_state(self, user_id: int, input_id: str, filter: str = "any"):
        state = await self.session.get_state(user_id)
        if not state:
            return
        state["input_id"] = input_id
        state["filter"] = filter
        await self.session.set_state(user_id, state)

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
        asyncio.run(self._run())

    async def _run(self):
        print("Registered routes:", self.menu_registry.keys(), ", action commands:", self.action_commands.keys())
        await self.startup()
        await self.dp.start_polling(self.bot)
        
