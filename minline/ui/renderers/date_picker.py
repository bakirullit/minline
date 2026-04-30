"""Date picker question renderer - calendar UI."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from minline.ui.renderers.base import BaseRenderer
from datetime import datetime, timedelta


class DatePickerRenderer(BaseRenderer):
    """Renders date picker - calendar grid with navigation."""
    
    def render(self, question, show_back: bool = False) -> InlineKeyboardMarkup:
        """Render calendar for date selection."""
        # Get current month or from config
        current_date = question.config.get("current_date", datetime.now())
        year = current_date.year
        month = current_date.month
        
        # Month header
        buttons = [[InlineKeyboardButton(
            text=f"{datetime(year, month, 1).strftime('%B %Y')}",
            callback_data="__noop"
        )]]
        
        # Day headers
        buttons.append([
            InlineKeyboardButton(text=day, callback_data="__noop")
            for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        ])
        
        # First day of month
        first_day = datetime(year, month, 1)
        start_weekday = first_day.weekday()
        
        # Days of month
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        day_buttons = []
        
        # Empty cells for days before month starts
        day_buttons.extend([InlineKeyboardButton(text=" ", callback_data="__noop")] * start_weekday)
        
        # Day buttons
        for day in range(1, days_in_month + 1):
            day_buttons.append(InlineKeyboardButton(
                text=str(day),
                callback_data=f"__date_{year}_{month}_{day}"
            ))
        
        # Arrange in weeks (7 columns)
        for i in range(0, len(day_buttons), 7):
            buttons.append(day_buttons[i:i+7])
        
        # Navigation
        prev_month = datetime(year, month - 1, 1) if month > 1 else datetime(year - 1, 12, 1)
        next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        
        buttons.append([
            InlineKeyboardButton(text="◀", callback_data=f"__prev_month_{prev_month.year}_{prev_month.month}"),
            InlineKeyboardButton(text="Today", callback_data="__today"),
            InlineKeyboardButton(text="▶", callback_data=f"__next_month_{next_month.year}_{next_month.month}"),
        ])
        
        if show_back:
            buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="__back")])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def parse_input(self, input_event) -> str:
        """Parse date selection (YYYY-MM-DD format)."""
        if input_event.type == "callback" and input_event.value.startswith("__date_"):
            parts = input_event.value.split("_")
            year, month, day = int(parts[1]), int(parts[2]), int(parts[3])
            return f"{year}-{month:02d}-{day:02d}"
        raise TypeError(f"Invalid date picker input: {input_event.type}")
