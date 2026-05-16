#!/usr/bin/env python3
"""
Minline: Form with Different Question Types

Demonstrates all renderer types:
- text: Free text input
- single_choice: Numbered buttons (1, 2, 3...)
- multi_choice: Toggle buttons with submit
- date_picker: Calendar UI

Key concepts:
- Question type determines UI rendering
- config dict holds type-specific data (items, etc.)
- Framework handles all UI generation
"""

from minline import (
    MinlineApp,
    Menu,
    Button,
    Question,
    Form,
    InputEvent,
    ValidationResult,
)

# Your Telegram bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize app
app = MinlineApp(BOT_TOKEN)


# ============= VALIDATORS =============

def validate_selection(event: InputEvent) -> ValidationResult:
    """Validate user selected an option."""
    try:
        choice = int(event.value)
        if choice < 1 or choice > 3:
            return ValidationResult(
                ok=False,
                error="❌ Please select option 1, 2, or 3",
                code="INVALID_CHOICE"
            )
        return ValidationResult(ok=True)
    except ValueError:
        return ValidationResult(
            ok=False,
            error="❌ Please enter a number",
            code="NOT_A_NUMBER"
        )


def validate_interests(event: InputEvent) -> ValidationResult:
    """Validate multi-choice selection (just accept for now)."""
    return ValidationResult(ok=True)


def validate_date(event: InputEvent) -> ValidationResult:
    """Validate date format."""
    # Input is YYYY-MM-DD from date picker
    date_str = event.value
    try:
        parts = date_str.split("-")
        if len(parts) != 3:
            raise ValueError()
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        if month < 1 or month > 12 or day < 1 or day > 31:
            raise ValueError()
        return ValidationResult(ok=True)
    except (ValueError, IndexError):
        return ValidationResult(
            ok=False,
            error="❌ Invalid date format",
            code="INVALID_DATE"
        )


# ============= QUESTIONS WITH DIFFERENT TYPES =============

# TYPE 1: TEXT (free input)
name_question = Question(
    id="name",
    type="text",
    text="👤 What's your name?",
)

# TYPE 2: SINGLE_CHOICE (numbered buttons)
status_question = Question(
    id="status",
    type="single_choice",
    text="💼 What's your employment status?",
    validator=validate_selection,
    renderer="single_choice",
    config={
        "items": [
            "👨‍💼 Employed",
            "🎓 Student",
            "🔍 Looking for work",
        ]
    }
)

# TYPE 3: MULTI_CHOICE (toggle buttons + submit)
interests_question = Question(
    id="interests",
    type="multi_choice",
    text="🎯 What are your interests? (select at least one)",
    validator=validate_interests,
    renderer="multi_choice",
    config={
        "items": [
            "💻 Technology",
            "🎨 Art & Design",
            "📚 Education",
            "⚽ Sports",
            "🎮 Gaming",
        ],
        "selected": set(),  # Tracks selected indices
    }
)

# TYPE 4: DATE_PICKER (calendar UI)
date_question = Question(
    id="preferred_date",
    type="date_picker",
    text="📅 When would you like to meet?",
    validator=validate_date,
    renderer="date_picker",
    config={}
)

# TYPE 5: SINGLE_CHOICE EXAMPLE 2
country_question = Question(
    id="country",
    type="single_choice",
    text="🌍 Which country are you from?",
    renderer="single_choice",
    config={
        "items": [
            "🇰🇿 Kazakhstan",
            "🇷🇺 Russia",
            "🇺🇸 United States",
            "🇬🇧 United Kingdom",
            "🇨🇭 Other",
        ]
    }
)


# ============= CREATE FORM =============

survey_form = Form(
    id="survey",
    questions=[
        name_question,
        status_question,
        interests_question,
        date_question,
        country_question,
    ],
)


# ============= ATTACH FORM =============

app.workflow = survey_form


# ============= ROUTES =============

@app.route("/")
def home():
    return Menu(
        menu_id="home",
        text="🏠 Minline - Question Types Example\n\nTry our survey with different question types!",
        controls=[
            Button("📋 Start Survey", route="/survey/start"),
        ]
    )


@app.route("/survey/start")
def survey_start():
    return Menu(
        menu_id="survey_start",
        text="📋 Quick Survey\n\nWe'll show you:\n• Text input\n• Single choice (buttons)\n• Multi-choice (toggles)\n• Date picker\n\nLet's go!",
        controls=[
            Button("▶️ Start", route="/survey/begin"),
        ]
    )


@app.route("/survey/begin")
def survey_begin():
    return Menu(
        menu_id="survey_begin",
        text="Getting first question...",
        controls=[],
    )


@app.route("/survey/complete")
def survey_complete():
    return Menu(
        menu_id="survey_complete",
        text="✅ Survey Complete!\n\nThank you for your answers!",
        controls=[
            Button("🏠 Home", route="/"),
        ]
    )


# ============= QUESTION TYPE REFERENCE =============

"""
QUESTION TYPES & RENDERERS:

1. TEXT (TextRenderer)
   ├─ Free-form user input
   ├─ No buttons
   ├─ config: {} (empty)
   └─ Input: Plain text

2. SINGLE_CHOICE (SingleChoiceRenderer)
   ├─ Numbered buttons (1️⃣, 2️⃣, 3️⃣...)
   ├─ User sends number or clicks button
   ├─ config: {"items": ["Option A", "Option B", ...]}
   └─ Input: Number (1-based)

3. MULTI_CHOICE (MultiChoiceRenderer)
   ├─ Toggle buttons with checkboxes (✅/☐)
   ├─ Submit button when done
   ├─ config: {"items": [...], "selected": set()}
   └─ Input: List of selected indices

4. DATE_PICKER (DatePickerRenderer)
   ├─ Calendar UI with month navigation
   ├─ Day selection
   ├─ config: {} (optional current_date)
   └─ Input: "YYYY-MM-DD"

CUSTOM RENDERERS:
   • Implement BaseRenderer
   • Add to registry: register_renderer("custom", MyRenderer())
   • Use: type="custom" with your Question
"""


if __name__ == "__main__":
    app.run()
