from minline import MinlineApp, Menu, Button

app = MinlineApp("TELEGRAM_BOT_TOKEN")

# Root menu
@app.route("/")
def main():
    return Menu(
        menu_id="main",
        controls=[
            [Button("Settings", "#route:/settings")],
            [Button("Profile", "#route:/profile")],
            [Button("Help", "#route:/help")]
        ]
    )

# Settings menu with relative routing
@app.route("/settings")
def settings():
    return Menu(
        menu_id="settings",
        controls=[
            [Button("Notifications", "#route:notifications")],
            [Button("Privacy", "#route:privacy")]
        ]
    )

@app.route("/settings/notification")
def notifications():
    return Menu(
        menu_id="notifications",
        controls=[
            [Button("Enable All", "toggle_all_notifications")],
        ]
    )

@app.route("/settings/privacy")
def privacy():
    return Menu(
        menu_id="privacy",
        controls=[
            [Button("Show Profile to Everyone", "toggle_profile_visibility")],
        ]
    )

# Profile menu
@app.route("/profile")
def profile():
    return Menu(
        menu_id="profile",
        controls=[
            [Button("Edit Profile", "edit_profile")],
            [Button("View Stats", "view_stats")],
        ]
    )

# Help menu demonstrating 404 fallback
@app.route("/help")
def help_menu():
    return Menu(
        menu_id="help",
        controls=[
            [Button("FAQ", "#route:/help/faq")],
            [Button("Contact Support", "#route:/help/contact")],
            [Button("Broken Link Test", "#route:/does-not-exist")]
        ]
    )

@app.route("/help/faq")
def faq():
    return Menu(
        menu_id="faq",
        controls=[
            [Button("What is this bot?", "faq_what_is")],
            [Button("How to use it?", "faq_how_to_use")]
        ]
    )

@app.route("/help/contact")
def contact():
    return Menu(
        menu_id="contact",
        controls=[
            [Button("Send Email", "send_email")]
        ]
    )

# Run the bot
app.run()