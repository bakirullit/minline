#!/usr/bin/env python3
"""
Back button behavior in Minline.

Demonstrates:
- Automatic back button (enabled by default)
- Navigation stack (back button remembers previous menus)
- back=False to disable back button for specific menus
- Manual back button: #route:// 

The back button is automatically shown when:
1. Current route is not '/'
2. back=True (default)

Back navigation works via NavigationStack which tracks user's journey.
"""

from minline import MinlineApp, Menu, Button

app = MinlineApp("BOT_TOKEN")


@app.route("/")
def root():
    return Menu(
        menu_id="root",
        text="🏠 Home",
        controls=[
            [Button("Level 1", "#route:/level1")],
            [Button("Deep Path", "#route:/level1/level2/level3")]
        ]
    )


@app.route("/level1")
def level1():
    # back=True (default) - user can go back to /
    return Menu(
        menu_id="level1",
        text="📍 Level 1",
        controls=[
            [Button("Go Deeper", "#route:level2")],
            [Button("Sibling", "#route:/level1_alt")]
        ]
    )


@app.route("/level1_alt")
def level1_alt():
    return Menu(
        menu_id="level1_alt",
        text="📍 Level 1 Alternative",
        controls=[
            [Button("Back to Level 1", "#route:/level1")]
        ]
    )


@app.route("/level1/level2")
def level2():
    # back=True (default) - user can go back to /level1
    return Menu(
        menu_id="level2",
        text="📍 Level 2",
        controls=[
            [Button("Go Even Deeper", "#route:level3")],
        ]
    )


@app.route("/level1/level2/level3")
def level3():
    # back=True (default) - user can go back to /level1/level2
    return Menu(
        menu_id="level3",
        text="📍 Level 3 (Deep)",
        controls=[
            [Button("Fullscreen Mode", "#route:/fullscreen")]
        ]
    )


@app.route("/fullscreen")
def fullscreen():
    # back=False - no automatic back button
    # User must click "Exit" to leave
    return Menu(
        menu_id="fullscreen",
        text="🎮 Fullscreen Content\n\nThis menu has no back button!",
        controls=[
            [Button("📤 Exit Fullscreen", "#route:/")],
        ],
        back=False  # Disable automatic back button
    )


@app.route("/wizard")
def wizard_start():
    # Wizard pattern: step 1
    return Menu(
        menu_id="wizard_step1",
        text="🧙 Wizard - Step 1/3\n\nEnter your name:",
        controls=[
            [Button("Skip", "#route:/")]
        ],
        back=False  # Users must complete wizard or skip
    )


@app.route("/wizard/step2")
def wizard_step2():
    # Wizard pattern: step 2
    return Menu(
        menu_id="wizard_step2",
        text="🧙 Wizard - Step 2/3\n\nChoose your category:",
        controls=[
            [Button("Category A", "#route:step3")],
            [Button("Category B", "#route:step3")],
            [Button("❌ Cancel Wizard", "#route:/")]
        ],
        back=False
    )


@app.route("/wizard/step2/step3")
def wizard_step3():
    # Wizard pattern: final step
    return Menu(
        menu_id="wizard_step3",
        text="🧙 Wizard - Step 3/3\n\nConfirm setup:",
        controls=[
            [Button("✅ Complete", "#route:/")],
            [Button("❌ Start Over", "#route:/wizard")]
        ],
        back=False
    )


if __name__ == "__main__":
    app.run()
