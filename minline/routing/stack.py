import time


class NavigationStack:
    """Manages navigation history for users with TTL-based cleanup."""
    
    def __init__(self, ttl_seconds: int = 86400):
        """
        Initialize navigation stack.
        
        Args:
            ttl_seconds: Time to live for user stacks (default: 24 hours)
        """
        self.stack = {}
        self.timestamps = {}  # Track when each user's stack was last accessed
        self.ttl = ttl_seconds

    def _cleanup_expired(self):
        """Remove stacks that have exceeded TTL."""
        current_time = time.time()
        expired = [
            chat_id for chat_id, ts in self.timestamps.items()
            if current_time - ts > self.ttl
        ]
        for chat_id in expired:
            self.stack.pop(chat_id, None)
            self.timestamps.pop(chat_id, None)

    def _update_timestamp(self, chat_id: int):
        """Update last access time for a user."""
        self.timestamps[chat_id] = time.time()

    def push(self, chat_id: int, path: str):
        self._cleanup_expired()
        self._update_timestamp(chat_id)
        self.stack.setdefault(chat_id, [])
        if not self.stack[chat_id] or self.stack[chat_id][-1] != path:
            self.stack[chat_id].append(path)

    def back(self, chat_id: int):
        self._cleanup_expired()
        self._update_timestamp(chat_id)
        if chat_id not in self.stack or len(self.stack[chat_id]) <= 1:
            return "/"
        self.stack[chat_id].pop()
        return self.stack[chat_id][-1]

    def current(self, chat_id: int):
        self._cleanup_expired()
        self._update_timestamp(chat_id)
        if chat_id not in self.stack or not self.stack[chat_id]:
            return "/"
        return self.stack[chat_id][-1]
