import json
from typing import Any


class RatesRepository:
    def __init__(self, redis):
        self._redis = redis

    async def get_all_by_key(self, key: str):
        return await self._redis.hgetall(key)

    async def get_by_key(self, key: str, field: str):
        return await self._redis.hget(key, field)

    async def set_by_key_field(self, key: str, field: str, value: Any):
        return await self._redis.hset(key, field, value)

    async def load_data(self):
        await self._redis.hset('kgd-led', '10:30',
                               json.dumps(
                                   {"adult": 1500, "teen": 850, "kid": 200, "luggage": 100, "pet": 500, "total": 450}))
        await self._redis.hset('kgd-led', '21:15',
                               json.dumps(
                                   {"adult": 3000, "teen": 900, "kid": 350, "luggage": 75, "pet": 300, "total": 200}))
        await self._redis.hset('kgd-led', '13:00',
                               json.dumps(
                                   {"adult": 2000, "teen": 850, "kid": 200, "luggage": 100, "pet": 600, "total": 580}))
        await self._redis.hset('kgd-msw', '8:20',
                               json.dumps(
                                   {"adult": 3500, "teen": 1850, "kid": 550, "luggage": 170, "pet": 500, "total": 580}))
        await self._redis.hset('kgd-msw', '23:15',
                               json.dumps(
                                   {"adult": 2000, "teen": 700, "kid": 350, "luggage": 100, "pet": 300, "total": 580}))
