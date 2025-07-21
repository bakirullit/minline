from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from minline import MinlineApp, Menu, Button

BOT_TOKEN = "your_token_here"
app = MinlineApp(BOT_TOKEN)

@app.menu("main")
def main_menu():
    return Menu(
        text_id="main_title",
        controls=[
            [Button("Open profile", "open_profile")],
            [Button("Settings", "open_settings")]
        ]
    )

@app.menu("main/settings")
def settings_menu():
    return Menu(
        text_id="settings_title",
        controls=[
            [Button("Back", "#route://")]
        ]
    )

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(app.router)

@dp.message(commands=["start"])
async def start_handler(message: Message):
    await app.open(message.chat.id, "main")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(app.bot))
