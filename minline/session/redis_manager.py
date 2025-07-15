import json
import redis.asyncio as redis

class RedisSessionManager:
    def __init__(self, host='localhost', port=6379, db=0, prefix="session:"):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.prefix = prefix

    def _key(self, user_id: int):
        return f"{self.prefix}{user_id}"

    async def set_state(self, user_id: int, data: dict, ttl: int = None):
        raw = json.dumps(data)
        await self.redis.set(self._key(user_id), raw, ex=ttl)

    async def get_state(self, user_id: int) -> dict | None:
        raw = await self.redis.get(self._key(user_id))
        if raw:
            return json.loads(raw)
        return None

    async def delete_state(self, user_id: int):
        await self.redis.delete(self._key(user_id))
