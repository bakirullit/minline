#!/usr/bin/env python3
"""
Minline: Multi-Step Form Example

Demonstrates a complete multi-step registration form using Questions and Form.

Key concepts:
- Define Questions with validators
- Compose into Form
- Attach Form to app
- Framework handles progression automatically
"""

import re
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

def email_validator(event: InputEvent) -> ValidationResult:
    """Validate email format."""
    email = event.value.strip()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return ValidationResult(
            ok=False,
            error="❌ Invalid email format",
            code="INVALID_EMAIL"
        )
    return ValidationResult(ok=True)


def phone_validator(event: InputEvent) -> ValidationResult:
    """Validate phone (at least 10 digits)."""
    phone = event.value.replace(" ", "").replace("-", "").replace("+", "")
    
    if not phone.isdigit():
        return ValidationResult(
            ok=False,
            error="❌ Phone must contain only digits (and +, -, spaces)",
            code="INVALID_PHONE_CHARS"
        )
    
    if len(phone) < 10:
        return ValidationResult(
            ok=False,
            error="❌ Phone too short (need at least 10 digits)",
            code="PHONE_TOO_SHORT"
        )
    
    return ValidationResult(ok=True)


def age_validator(event: InputEvent) -> ValidationResult:
    """Validate age is between 18 and 100."""
    try:
        age = int(event.value.strip())
    except ValueError:
        return ValidationResult(
            ok=False,
            error="❌ Please enter a number",
            code="NOT_A_NUMBER"
        )
    
    if age < 18:
        return ValidationResult(
            ok=False,
            error="❌ Must be 18 or older",
            code="TOO_YOUNG"
        )
    
    if age > 120:
        return ValidationResult(
            ok=False,
            error="❌ Age seems unrealistic",
            code="TOO_OLD"
        )
    
    return ValidationResult(ok=True)


# ============= DEFINE QUESTIONS =============

email_question = Question(
    id="email",
    type="text",
    text="📧 Enter your email:",
    validator=email_validator,
)

phone_question = Question(
    id="phone",
    type="text",
    text="☎️ Enter your phone number:",
    validator=phone_validator,
)

age_question = Question(
    id="age",
    type="text",
    text="🎂 How old are you?",
    validator=age_validator,
)

name_question = Question(
    id="name",
    type="text",
    text="👤 What is your full name?",
    # No validator - accept any name
)


# ============= CREATE FORM =============

registration_form = Form(
    id="registration",
    questions=[email_question, phone_question, age_question, name_question],
)


# ============= ATTACH FORM TO APP =============

app.workflow = registration_form


# ============= ROUTES =============

@app.route("/")
def home():
    return Menu(
        menu_id="home",
        text="🏠 Welcome to Registration\n\nLet's get your information!",
        controls=[
            Button("📝 Start Registration", route="/form/start"),
            Button("❌ Reset Form", route="/form/reset"),
        ]
    )


@app.route("/form/start")
def form_start():
    return Menu(
        menu_id="form_start",
        text="📝 Registration Form\n\nWe'll ask for:\n• Email\n• Phone\n• Age\n• Name\n\nClick button when ready!",
        controls=[
            Button("▶️ Begin", route="/form/next"),
        ]
    )


@app.route("/form/next")
def form_next():
    """Triggered when user clicks Begin - framework will ask first question."""
    return Menu(
        menu_id="form_next",
        text="Getting first question...",
        controls=[],
    )


@app.route("/form/complete")
def form_complete():
    return Menu(
        menu_id="form_complete",
        text="✅ Registration Complete!\n\nThank you for your information. Your registration has been saved.",
        controls=[
            Button("🏠 Home", route="/"),
        ]
    )


@app.route("/form/reset")
def form_reset():
    return Menu(
        menu_id="form_reset",
        text="🔄 Form has been reset.\n\nStart fresh whenever you're ready!",
        controls=[
            Button("📝 Start Again", route="/form/start"),
            Button("🏠 Home", route="/"),
        ]
    )


# ============= HOW IT WORKS =============

"""
FRAMEWORK FLOW:

1. User clicks /form/start → form_start() menu shown
2. User clicks "Begin" → /form/next route triggered
3. Framework checks app.workflow (our Form)
4. Gets first question (email_question) from form
5. Calls app._ask_question(chat_id, email_question)
6. Renders question with validator
7. User enters input → InputEvent created
8. Framework calls email_question.validate_input(InputEvent)
9. If ValidationResult.ok=False:
   - Show error message
   - Ask same question again
10. If ValidationResult.ok=True:
   - Store answer in form
   - Get next question (phone_question)
   - Ask it
11. Repeat for all questions
12. After last question answered:
   - Detect form complete
   - Show /form/complete menu
   - Reset form state

DEVELOPER DOES:
✅ Define validators
✅ Create Questions
✅ Compose Form
✅ Attach to app
✅ Define menus

FRAMEWORK DOES:
✅ Ask questions in order
✅ Validate answers
✅ Show validation errors
✅ Detect completion
✅ Store data in session
✅ Reset state
"""


if __name__ == "__main__":
    app.run()
