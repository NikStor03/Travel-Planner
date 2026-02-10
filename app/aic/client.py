import time
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._store: Dict[str, tuple[float, Any]] = {}

    def get(self, key: str):
        item = self._store.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any):
        self._store[key] = (time.time() + self.ttl, value)

class AICClient:
    def __init__(self):
        self.base_url = settings.aic_base_url
        self.timeout = settings.aic_timeout_seconds
        self.cache = TTLCache(ttl_seconds=300)

    async def get_artwork(self, external_id: int) -> Optional[dict]:
        cache_key = f"artwork:{external_id}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/artworks/{external_id}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(url)

        if resp.status_code == 404:
            self.cache.set(cache_key, None)
            return None
        resp.raise_for_status()
        data = resp.json().get("data")
        self.cache.set(cache_key, data)
        return data
