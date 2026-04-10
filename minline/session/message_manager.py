from .base import SessionManager

class MessageManager:
    def __init__(self, session: SessionManager):
        self.session = session

    async def get(self, chat_id: int):
        return await self.session.get(chat_id, f"menu_{chat_id}")

    async def set(self, chat_id: int, message_id: int):
        await self.session.set(chat_id, f"menu_{chat_id}", message_id)

    async def clear(self, chat_id: int):
        await self.session.set(chat_id, f"menu_{chat_id}", None)
