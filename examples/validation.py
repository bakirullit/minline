#!/usr/bin/env python3
"""
Question & Form example for Minline.

Demonstrates:
- Questions work STANDALONE
- Questions work INSIDE Forms
- Validators are fully user-owned
- Form as thin orchestration layer
- Framework handles Question lifecycle (no aiogram needed!)

Key principle: Question is the primitive, Form just chains them.
"""

import re
import logging
from minline import (
    MinlineApp,
    Menu,
    Button,
    Question,
    InputEvent,
    ValidationResult,
    Form,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize app
app = MinlineApp(BOT_TOKEN)


# ============= CUSTOM VALIDATORS =============

def email_validator(value: str) -> ValidationResult:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        return ValidationResult(
            ok=False,
            error="❌ Invalid email format. Please try again.",
            code="INVALID_EMAIL"
        )
    return ValidationResult(ok=True)


# ============= STANDALONE QUESTIONS (can work alone OR in a form) =============

def email_validator(input_event: InputEvent) -> ValidationResult:
    """User-defined validator - framework just executes and reacts to result."""
    email = input_event.value
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return ValidationResult(ok=False, error="❌ Invalid email format", code="INVALID_EMAIL")
    
    return ValidationResult(ok=True)


def phone_validator(input_event: InputEvent) -> ValidationResult:
    """Phone validator - Kazakh number example."""
    phone = input_event.value
    pattern = r'^[0-9\+\-\s()]{10,}$'
    
    if not re.match(pattern, phone):
        return ValidationResult(ok=False, error="❌ Invalid phone format", code="INVALID_PHONE")
    
    return ValidationResult(ok=True)


def age_validator(input_event: InputEvent) -> ValidationResult:
    """Age validator - must be 18+."""
    try:
        age = int(input_event.value)
        if age < 18:
            return ValidationResult(ok=False, error="❌ Must be 18 or older", code="TOO_YOUNG")
        if age > 150:
            return ValidationResult(ok=False, error="❌ Invalid age", code="INVALID_AGE")
        return ValidationResult(ok=True)
    except ValueError:
        return ValidationResult(ok=False, error="❌ Please enter a number", code="NOT_A_NUMBER")


# Create standalone questions
email_question = Question(
    id="email",
    type="text",
    text="📧 Enter your email:",
    validator=email_validator,
)

phone_question = Question(
    id="phone",
    type="text",
    text="☎️ Enter your phone:",
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
    text="👤 What's your full name?",
)


# ============= FORM (optional orchestration of questions) =============

registration_form = Form(
    id="registration",
    questions=[email_question, phone_question, age_question, name_question],
)


# ============= ROUTES (Minline menus) =============

@app.route("/")
def main_menu():
    return Menu(
        menu_id="main",
        text="🏠 Welcome to Minline\n\nQuestions-based interaction runtime.",
        controls=[
            Button("📝 Start Registration", route="/form/start"),
        ]
    )


@app.route("/form/start")
def form_start():
    return Menu(
        menu_id="form_start",
        text="📝 Registration Form\n\nClick start to begin.",
        controls=[
            Button("▶️ Start", route="/form/next"),
        ]
    )


@app.route("/form/next")
def form_next():
    """Handler for starting form - framework will ask first question."""
    return Menu(
        menu_id="form_next",
        text="Getting first question...",
        controls=[],
    )


@app.route("/form/complete")
def form_complete():
    return Menu(
        menu_id="form_complete",
        text="✅ Registration Complete!\n\nThank you!",
        controls=[
            Button("🏠 Home", route="/"),
        ]
    )


# ============= ATTACH FORM TO APP =============

app.workflow = registration_form


if __name__ == "__main__":
    app.run()
