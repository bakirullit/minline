#!/usr/bin/env python3
"""
Disabling back button for specific menus.

Demonstrates:
- back=False parameter to hide automatic back button
- Manual back button with #route:// or #route:/
- Use case: fullscreen content, modal dialogs, wizard flows
"""

from minline import MinlineApp, Menu, Button

app = MinlineApp("BOT_TOKEN")


@app.route("/")
def main():
    return Menu(
        menu_id="main",
        text="🎮 Application",
        controls=[
            [Button("📸 Fullscreen Gallery", "#route:/gallery")],
            [Button("⚙️ Settings", "#route:/settings")],
        ]
    )


@app.route("/gallery")
def gallery():
    # Fullscreen mode - hide back button
    return Menu(
        menu_id="gallery",
        text="📸 Fullscreen Gallery\n\nUse buttons to navigate",
        controls=[
            [Button("⬅️ Previous", "#route:/")],
            [Button("➡️ Next", "#route:/")],
            [Button("❌ Exit", "#route:/")],
        ],
        back=False  # No automatic back button
    )


@app.route("/settings")
def settings():
    return Menu(
        menu_id="settings",
        text="⚙️ Settings",
        controls=[
            [Button("🔔 Notifications", "#route:notifications")],
            [Button("🔐 Privacy", "#route:privacy")],
        ]
    )


@app.route("/settings/notifications")
def notifications():
    return Menu(
        menu_id="notifications",
        text="🔔 Notifications\n\nEnable notifications?",
        controls=[
            [Button("✅ Enable", "#route:enabled")],
            [Button("❌ Disable", "#route:disabled")],
        ],
        back=False  # Modal dialog - must choose
    )


@app.route("/settings/notifications/enabled")
def notifications_enabled():
    return Menu(
        menu_id="enabled",
        text="✅ Notifications Enabled",
        controls=[
            [Button("🔙 Back to Settings", "#route:/settings")],
        ],
        back=False
    )


@app.route("/settings/notifications/disabled")
def notifications_disabled():
    return Menu(
        menu_id="disabled",
        text="❌ Notifications Disabled",
        controls=[
            [Button("🔙 Back to Settings", "#route:/settings")],
        ],
        back=False
    )


@app.route("/settings/privacy")
def privacy():
    return Menu(
        menu_id="privacy",
        text="🔐 Privacy\n\nWho can see your profile?",
        controls=[
            [Button("🌍 Public", "#route:public")],
            [Button("👥 Friends Only", "#route:friends")],
            [Button("🔒 Private", "#route:private")],
        ],
        back=False  # Must select an option
    )


@app.route("/settings/privacy/public")
def privacy_public():
    return Menu(
        menu_id="public",
        text="🌍 Profile is now public",
        controls=[
            [Button("🔙 Back", "#route:/settings")],
        ],
        back=False
    )


@app.route("/settings/privacy/friends")
def privacy_friends():
    return Menu(
        menu_id="friends",
        text="👥 Profile visible to friends only",
        controls=[
            [Button("🔙 Back", "#route:/settings")],
        ],
        back=False
    )


@app.route("/settings/privacy/private")
def privacy_private():
    return Menu(
        menu_id="private",
        text="🔒 Profile is private",
        controls=[
            [Button("🔙 Back", "#route:/settings")],
        ],
        back=False
    )


if __name__ == "__main__":
    app.run()
