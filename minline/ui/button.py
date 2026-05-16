from aiogram.types import InlineKeyboardButton


class Button:
    def __init__(self, text: str, callback: str = None, url: str = None, route: str = None):
        self.text = text
        self.callback = callback
        self.url = url
        self.route = route

    def render(self):
        # Convert route to callback format
        if self.route:
            callback_data = f"__route:{self.route}"
            if len(callback_data.encode()) > 64:
                raise ValueError("route callback_data exceeds 64 bytes")
            return InlineKeyboardButton(text=self.text, callback_data=callback_data)
        
        if self.callback and len(self.callback.encode()) > 64:
            raise ValueError("callback_data exceeds 64 bytes")
        
        if self.url:
            return InlineKeyboardButton(text=self.text, url=self.url)
        
        return InlineKeyboardButton(text=self.text, callback_data=self.callback)
