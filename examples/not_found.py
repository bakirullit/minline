#!/usr/bin/env python3
"""
404 Error handling in Minline.

Demonstrates:
- Unknown routes show a 404 menu automatically
- Navigation stack is preserved (back still works)
- 404 doesn't crash the bot
- User can navigate away from 404 menu

Key behavior:
  1. User clicks unknown route
  2. is_404 flag is set
  3. Menu.not_found(path) is shown
  4. Back button returns to previous menu (not 404)
  5. Navigation continues normally
"""

from minline import MinlineApp, Menu, Button

app = MinlineApp("BOT_TOKEN")


@app.route("/")
def main():
    return Menu(
        menu_id="main",
        text="🏠 Main Menu",
        controls=[
            [Button("✅ Valid Route", "#route:/valid")],
            [Button("❌ Broken Route", "#route:/does-not-exist")],
            [Button("🎯 Test 404", "#route:/some/deep/broken/path")],
        ]
    )


@app.route("/valid")
def valid():
    return Menu(
        menu_id="valid",
        text="✅ This is a valid route",
        controls=[
            [Button("Back to Home", "#route:/")],
            [Button("Try Another 404", "#route:/another-broken-route")],
        ]
    )


if __name__ == "__main__":
    app.run()
