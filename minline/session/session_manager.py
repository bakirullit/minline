import json
import aiosqlite
import time

class SQLiteSessionManager:
    def __init__(self, db_path="local.db"):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    user_id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL,
                    expires_at INTEGER
                )
            """)
            await db.commit()

    async def _is_expired(self, expires_at: int | None) -> bool:
        return expires_at is not None and expires_at < int(time.time())

    async def set_state(self, user_id: int, data: dict, ttl: int = None):
        expires_at = int(time.time()) + ttl if ttl else None
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO sessions (user_id, data, expires_at)
                VALUES (?, ?, ?)
            """, (user_id, json.dumps(data), expires_at))
            await db.commit()

    async def get_state(self, user_id: int) -> dict | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT data, expires_at FROM sessions WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    data, expires_at = row
                    if await self._is_expired(expires_at):
                        await self.delete_state(user_id)
                        return None
                    return json.loads(data)
        return None

    async def delete_state(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
            await db.commit()
