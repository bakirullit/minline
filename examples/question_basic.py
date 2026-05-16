#!/usr/bin/env python3
"""
Minline: Standalone Question Example

Demonstrates a single Question used independently (not in a Form).

Key concepts:
- Question is an atomic interaction primitive
- Can be used standalone without Form
- Has optional validator
- Framework handles asking and validating
"""

from minline import MinlineApp, Menu, Button, Question, InputEvent, ValidationResult

# Your Telegram bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize app
app = MinlineApp(BOT_TOKEN)


# ============= DEFINE VALIDATOR =============

def email_validator(event: InputEvent) -> ValidationResult:
    """Validate email format."""
    email = event.value.strip()
    
    # Simple email check
    if "@" not in email or "." not in email:
        return ValidationResult(
            ok=False,
            error="❌ Invalid email (need @ and .)",
            code="INVALID_EMAIL_FORMAT"
        )
    
    # Check length
    if len(email) < 5:
        return ValidationResult(
            ok=False,
            error="❌ Email too short",
            code="EMAIL_TOO_SHORT"
        )
    
    return ValidationResult(ok=True)


# ============= DEFINE STANDALONE QUESTION =============

email_question = Question(
    id="email",
    type="text",
    text="📧 Please enter your email:",
    validator=email_validator,
    renderer="text",
    config={}
)


# ============= ROUTES =============

@app.route("/")
def home():
    return Menu(
        menu_id="home",
        text="🏠 Minline - Standalone Question Example\n\nClick button to verify your email.",
        controls=[
            Button("📧 Verify Email", route="/ask/email"),
            Button("ℹ️ About", route="/about"),
        ]
    )


@app.route("/ask/email")
def ask_email():
    """Handler for email question route."""
    return Menu(
        menu_id="ask_email",
        text="Starting email validation...",
        controls=[],
    )


@app.route("/about")
def about():
    return Menu(
        menu_id="about",
        text="ℹ️ About This Example\n\nDemonstrates a standalone Question:\n\n• Single interaction\n• User-defined validator\n• Framework handles asking\n• No Form needed",
        controls=[
            Button("🏠 Home", route="/"),
        ]
    )


# ============= MIDDLEWARE TO ACTIVATE QUESTION =============

# When user navigates to /ask/email route, activate the question
# (In real app, you'd hook this in route handler or middleware)

# For demo purposes, we'll show how to manually activate:
# In a real scenario, you'd do this when route is hit:
# app.active_questions[chat_id] = email_question
# await app._ask_question(chat_id, email_question)


if __name__ == "__main__":
    app.run()
