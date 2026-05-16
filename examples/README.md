#!/usr/bin/env python3
"""
Minline Examples Guide

This directory contains example applications demonstrating Minline features.

EXAMPLES:

1. question_basic.py
   └─ Standalone Question usage
   └─ Single email validation question
   └─ Shows: Question, validator, framework handling

2. form_registration.py
   └─ Multi-step registration form
   └─ 4 questions: email, phone, age, name
   └─ Shows: Form orchestration, progression, completion

3. form_renderers.py
   └─ All question types demonstrated
   └─ Text, single_choice, multi_choice, date_picker
   └─ Shows: Different UI renderers, configs

4. validation.py (original)
   └─ Full working example with setup
   └─ Shows: Complete app initialization


QUICK START:

1. Set your BOT_TOKEN in the example file:
   BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

2. Run the example:
   python3 examples/form_registration.py

3. Message your bot on Telegram to interact


CONCEPTS:

Question
├─ id: Unique identifier
├─ type: Renderer type (text, single_choice, multi_choice, date_picker)
├─ text: Question text shown to user
├─ validator: Optional validation function
├─ renderer: Renderer name (defaults to type)
└─ config: Type-specific configuration

Question Usage Modes:

Mode 1: STANDALONE
  question = Question(...)
  app.active_questions[chat_id] = question
  await app._ask_question(chat_id, question)
  # User answers once, done

Mode 2: IN FORM
  form = Form("id", [question1, question2, question3])
  app.workflow = form
  # Framework asks all questions in sequence
  # Validates each one
  # Shows errors and re-asks if validation fails
  # Detects completion and resets


Validator

Input:  InputEvent(type, value, meta)
Output: ValidationResult(ok, error, code)

Validator examples:

  def email_validator(event: InputEvent) -> ValidationResult:
      if "@" not in event.value:
          return ValidationResult(ok=False, error="No @", code="NO_AT")
      return ValidationResult(ok=True)

  # Access user info:
  chat_id = event.get_chat_id()
  user_id = event.get_user_id()


Form

  form = Form(
      id="survey",
      questions=[q1, q2, q3]
  )

  # Attach to app:
  app.workflow = form

  # Framework handles:
  # - Asking questions in order
  # - Validating answers
  # - Storing in session
  # - Detecting completion
  # - Resetting state

  # Developer can also manually use:
  current_q = await form.get_current_question_async(chat_id, session)
  next_q = await form.next_question_async(chat_id, session)
  await form.answer_question_async(chat_id, session, q_id, value)
  is_done = await form.is_complete_async(chat_id, session)
  data = await form.get_answers_async(chat_id, session)
  await form.reset_async(chat_id, session)


Renderers

TEXT
  config: {} (empty)
  Input: Plain text
  Example:
    Question("name", "text", "Name?")

SINGLE_CHOICE
  config: {"items": ["Option A", "Option B", "Option C"]}
  Input: Number (1-based)
  Buttons: 1️⃣ Option A, 2️⃣ Option B, 3️⃣ Option C
  Example:
    Question(
        "status",
        "single_choice",
        "Status?",
        config={"items": ["Student", "Worker", "Other"]}
    )

MULTI_CHOICE
  config: {"items": [...], "selected": set()}
  Input: List of indices
  Buttons: ✅/☐ toggles + submit
  Example:
    Question(
        "interests",
        "multi_choice",
        "Interests?",
        config={"items": ["Tech", "Art", "Sports"]}
    )

DATE_PICKER
  config: {} (or {"current_date": datetime.now()})
  Input: "YYYY-MM-DD"
  UI: Calendar with navigation
  Example:
    Question(
        "date",
        "date_picker",
        "Select date"
    )


CUSTOM RENDERER:

  from minline.ui.renderers import BaseRenderer, register_renderer
  from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

  class MyRenderer(BaseRenderer):
      def render(self, question, show_back=False):
          # Return InlineKeyboardMarkup
          pass
      
      def parse_input(self, input_event):
          # Parse Telegram input
          pass

  register_renderer("custom", MyRenderer())

  # Use:
  Question("id", "custom", "text?", renderer="custom")


FRAMEWORK FLOW:

When user sends message:

1. Check: Does user have active_question?
   
   YES ─────────────────────────────────────┐
   │                                        │
   ├─ Create InputEvent from message       │
   ├─ Call question.validate_input(event)  │
   │                                        │
   ├─ If ValidationResult.ok=False:        │
   │  └─ Show error + re-ask question      │
   │                                        │
   ├─ If ValidationResult.ok=True:         │
   │  ├─ Store answer in Form              │
   │  ├─ Get next question                 │
   │  ├─ If more questions: ask next       │
   │  ├─ If no more questions:             │
   │  │  ├─ Mark form complete             │
   │  │  ├─ Show /form/complete menu       │
   │  │  └─ Reset workflow state           │
   │  └─ Return                            │
   │                                        │
   NO ─────────────────────────────────────┘
   │
   └─ Normal routing: app._render("/custom")


API SUMMARY:

InputEvent:
  ├─ from_text(text, chat_id, user_id)
  ├─ from_number(value, chat_id, user_id)
  ├─ from_callback(data, chat_id, user_id)
  ├─ from_photo(file_id, chat_id, user_id, caption)
  ├─ from_document(file_id, chat_id, user_id, filename)
  ├─ get_chat_id()
  └─ get_user_id()

Question:
  ├─ validate_input(InputEvent) → ValidationResult
  └─ get_config(key, default)

ValidationResult:
  ├─ ok: bool
  ├─ error: str (optional)
  └─ code: str (optional)

Form:
  ├─ get_current_question_async(chat_id, session)
  ├─ next_question_async(chat_id, session)
  ├─ answer_question_async(chat_id, session, question_id, value)
  ├─ is_complete_async(chat_id, session)
  ├─ get_answers_async(chat_id, session)
  └─ reset_async(chat_id, session)

MinlineApp:
  ├─ workflow: Form (optional)
  ├─ active_questions: dict
  ├─ _ask_question(chat_id, question)
  └─ my_custom_handler() (auto-manages questions)


BEST PRACTICES:

1. Keep validators pure
   - No side effects
   - Deterministic (same input → same output)
   - Fast (network calls risky)

2. Use meaningful error messages
   - Help user understand what went wrong
   - Be specific, not vague
   - Example: ❌ Email must contain @ → ✅ "email@domain.com"

3. Compose reusable Questions
   - Don't create question inside Form
   - Define once, use many times
   - Makes testing easier

4. Use codes for tracking
   - Set code field in ValidationResult
   - Log codes to analytics
   - Don't rely on error text (user-facing)

5. Keep forms focused
   - Max 5-7 questions per form
   - Break into multiple forms if needed
   - Show progress

6. Use config for flexibility
   - Items, ranges, formats in config
   - Not hardcoded in Question definition
   - Easy to change later


DEBUGGING:

Enable logging:
  import logging
  logging.basicConfig(level=logging.DEBUG)

Check framework logs:
  - Question asking
  - Validation results
  - Form progression
  - Errors during message handling

Manual testing:
  # Test validator directly
  event = InputEvent.from_text("test@email.com", 123, 456)
  result = await question.validate_input(event)
  print(result)

  # Test Form progression
  form = Form("test", [q1, q2, q3])
  q = await form.get_current_question_async(123, session)
  await form.answer_question_async(123, session, "q1_id", "value")
  next_q = await form.next_question_async(123, session)


MIGRATION FROM OLD (Step/FormWorkflow):

OLD:
  step = Step("email", "Email?", validator=v)
  workflow = FormWorkflow([step])
  # Need custom message handler!

NEW:
  question = Question("email", "text", "Email?", validator=v)
  form = Form("form", [question])
  app.workflow = form
  # Framework handles everything!

Validator changes:
  OLD: def validator(value: str) → ValidationResult
  NEW: def validator(event: InputEvent) → ValidationResult
       event.value has the input
       Can access event.get_chat_id(), etc


PERFORMANCE NOTES:

- Questions cached in memory (fast)
- Session queries use SQLite (fast)
- Validation happens synchronously
- Rendering is stateless (efficient)
- No database queries by framework (your job)


For more help, see:
- ARCHITECTURE.md - System design
- MIGRATION_GUIDE.md - Old→New
- REFACTOR_SUMMARY.md - What changed
"""

if __name__ == "__main__":
    print(__doc__)
