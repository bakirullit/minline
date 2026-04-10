#!/usr/bin/env python3
"""
Basic example of Minline framework.

Demonstrates:
- Simple hierarchical menu structure
- Absolute and relative routing
- Session management with SqliteSessionManager
- Proper text vs menu_id usage
- Logging integration
- External links (url buttons)

Run with: python basic.py
"""

import logging
from minline import MinlineApp, Menu, Button
from minline.session import SqliteSessionManager

# Setup logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize app with SQLite session storage (safe for asyncio)
app = MinlineApp(
    token="YOUR_TELEGRAM_BOT_TOKEN",
    session_manager=SqliteSessionManager("bot_sessions.db")
)


# ============= ROOT MENU =============
@app.route("/")
def main():
    return Menu(
        menu_id="main",
        text="🏠 Main Menu",  # What user sees (text), not menu_id
        controls=[
            [Button("⚙️ Settings", "#route:/settings")],
            [Button("👤 Profile", "#route:/profile")],
            [Button("❓ Help", "#route:/help")]
        ]
    )


# ============= SETTINGS HIERARCHY =============
@app.route("/settings")
def settings():
    return Menu(
        menu_id="settings",
        text="⚙️ Settings",
        controls=[
            [Button("🔔 Notifications", "#route:notifications")],
            [Button("🔐 Privacy", "#route:privacy")]
        ]
    )


@app.route("/settings/notifications")
def notifications():
    return Menu(
        menu_id="notifications",
        text="🔔 Notification Settings",
        controls=[
            [Button("✅ Enable All", "#route:/")],
            [Button("❌ Disable All", "#route:/")],
        ]
    )


@app.route("/settings/privacy")
def privacy():
    return Menu(
        menu_id="privacy",
        text="🔐 Privacy Settings",
        controls=[
            [Button("🌍 Public", "#route:/")],
            [Button("🔒 Private", "#route:/")],
        ]
    )


# ============= PROFILE MENU =============
@app.route("/profile")
def profile():
    return Menu(
        menu_id="profile",
        text="👤 Your Profile",
        controls=[
            [Button("📝 Edit Profile", "#route:edit")],
            [Button("🔄 Change Avatar", "#route:avatar")]
        ]
    )


@app.route("/profile/edit")
def edit_profile():
    return Menu(
        menu_id="edit",
        text="📝 Edit Your Profile\n\nSend new bio:",
        controls=[]
    )


@app.route("/profile/avatar")
def change_avatar():
    return Menu(
        menu_id="avatar",
        text="🖼️ Upload new avatar",
        controls=[]
    )


# ============= HELP MENU =============
@app.route("/help")
def help_menu():
    return Menu(
        menu_id="help",
        text="❓ Help Center\n\nChoose a topic:",
        controls=[
            [Button("❓ FAQ", "#route:faq")],
            [Button("📞 Contact Support", "#route:support")],
            [Button("📚 Documentation", url="https://github.com/bakirullit/minline")]
        ]
    )


@app.route("/help/faq")
def faq():
    return Menu(
        menu_id="faq",
        text="❓ FAQ\n\n1. How to reset password?\n2. How to delete account?",
        controls=[]
    )


@app.route("/help/support")
def support():
    return Menu(
        menu_id="support",
        text="📞 Support\n\nEmail: support@example.com",
        controls=[
            [Button("📧 Send Email", url="mailto:support@example.com")]
        ]
    )


if __name__ == "__main__":
    app.run()