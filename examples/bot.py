from minline import MinlineApp, Menu, Button
from aiogram.types import CallbackQuery

BOT_TOKEN = "bot_token_here"  # Replace with your bot token

app = MinlineApp(BOT_TOKEN)

@app.route("/")
def main_menu():
    return Menu(
        menu_id="main",
        controls=[
            [Button("Settings", "#route:/settings")],
            [Button("Visit GitHub", url="https://github.com/bakirullit")]
        ]
    )

@app.route("/settings")
def settings_menu():
    return Menu(
        menu_id="settings",
        controls=[
            [Button("Say Hello!", "#say_hello")],
        ]
    )

@app.action("#say_hello")
async def say_hello_handler(callback: CallbackQuery, _: str):
    await callback.answer("Hello from action!", show_alert=True)

if __name__ == "__main__":
    app.run()
