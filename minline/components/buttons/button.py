class Button:
    def __init__(self, text_id: str, action: str = None, url: str = None, web_app_url: str = None, data: dict = None):
        self.text_id = text_id
        self.action = action
        self.url = url
        self.web_app_url = web_app_url
        self.data = data or {}
