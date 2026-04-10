import asyncio
import aiosqlite
from pathlib import Path

from minline.session.base import SessionManager


class SqliteSessionManager(SessionManager):
    """Async SQLite-based session manager safe for use in asyncio environments."""
    
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.lock = asyncio.Lock()
        self._initialized = False
        
    async def _init_db(self):
        """Initialize database schema."""
        if self._initialized:
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    chat_id INTEGER NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT,
                    PRIMARY KEY (chat_id, key)
                )
            """)
            await db.commit()
        self._initialized = True
    
    async def _ensure_init(self):
        """Ensure database is initialized before any operation."""
        if not self._initialized:
            await self._init_db()
    
    async def get(self, chat_id: int, key: str):
        """Get a session value."""
        await self._ensure_init()
        
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT value FROM sessions WHERE chat_id = ? AND key = ?",
                    (chat_id, key)
                )
                row = await cursor.fetchone()
                if row:
                    # Try to parse as JSON if it looks like JSON
                    import json
                    try:
                        return json.loads(row[0])
                    except (json.JSONDecodeError, TypeError):
                        return row[0]
                return None
    
    async def set(self, chat_id: int, key: str, value):
        """Set a session value."""
        await self._ensure_init()
        
        import json
        # Store as JSON string for flexibility
        value_str = json.dumps(value) if not isinstance(value, str) else value
        
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """
                    INSERT OR REPLACE INTO sessions (chat_id, key, value)
                    VALUES (?, ?, ?)
                    """,
                    (chat_id, key, value_str)
                )
                await db.commit()
    
    async def delete(self, chat_id: int, key: str):
        """Delete a session key."""
        await self._ensure_init()
        
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "DELETE FROM sessions WHERE chat_id = ? AND key = ?",
                    (chat_id, key)
                )
                await db.commit()
    
    async def clear(self, chat_id: int):
        """Clear all session data for a user."""
        await self._ensure_init()
        
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "DELETE FROM sessions WHERE chat_id = ?",
                    (chat_id,)
                )
                await db.commit()
