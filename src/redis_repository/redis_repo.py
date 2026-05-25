import json
from datetime import datetime

import typing

from typing import Optional, Union
from xml.dom.xmlbuilder import Options
from typing import Optional

# from src.routes.user import UserResponceModel

if typing.TYPE_CHECKING:
    from src.routes.subscription import SubscriptionOverview

class AnalyticsRedis:
    def __init__(self, client):
        self.client = client

    def get_user_cache(self, user_id: str) -> dict[str, Union["SubscriptionOverview", str]]:
        key = f"user:{user_id}:analytics"
        raw = self.client.get(key)
        return json.loads(raw) if raw else {}

    def get_last_updated(self, user_id: str) -> datetime | None:
        cache = self.get_user_cache(user_id)
        if "last_updated" in cache:
            return datetime.fromisoformat(cache["last_updated"])
        return None

    def set_user_cache(self, user_id: str, data: list["SubscriptionOverview"]):
        payload = {
            "last_updated": datetime.utcnow().isoformat(),
            "data": data
        }
        key = f"user:{user_id}:analytics"
        self.client.set(key, json.dumps(payload))

STORAGE_CACHE_TIME = 300

class RedisCache:
    def __init__(self, client) -> None:
        self.client = client

    def get(self, key: str):
        raw = self.client.get(key)
        return json.loads(raw) if raw else None

    def set(self, key: str, value, ttl: int):
        self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )

    def delete(self, key: str):
        self.client.delete(key)
