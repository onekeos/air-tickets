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

    async def get_hashes_by_mask(self, mask: str):
        return await self._redis.scan(match=mask)

    async def load_data(self):
        price_kgdled_1030: dict = {"adult": 1500, "teen": 850, "kid": 200, "luggage": 100, "pet": 500, "total": 450}
        price_kgdled_2115: dict = {"adult": 3000, "teen": 900, "kid": 350, "luggage": 75, "pet": 300, "total": 200}
        price_kgdled_1300: dict = {"adult": 2000, "teen": 850, "kid": 200, "luggage": 100, "pet": 600, "total": 580}
        price_kgdmsw_820: dict = {"adult": 3500, "teen": 1850, "kid": 550, "luggage": 170, "pet": 500, "total": 580}
        price_kgdmsw_2315: dict = {"adult": 2000, "teen": 700, "kid": 350, "luggage": 100, "pet": 300, "total": 580}
        await self._redis.hset('kgd-led,03-2022', '10:30', json.dumps(price_kgdled_1030))
        await self._redis.hset('kgd-led,03-2022', '21:15', json.dumps(price_kgdled_2115))
        await self._redis.hset('kgd-led,03-2022', '13:00', json.dumps(price_kgdled_1300))
        await self._redis.hset('kgd-led,04-2022', '10:30', json.dumps({k: v * 1.5 for k, v in price_kgdled_1030.items()}))
        await self._redis.hset('kgd-led,04-2022', '13:00', json.dumps({k: v * 1.5 for k, v in price_kgdled_1300.items()}))
        await self._redis.hset('kgd-led,04-2022', '21:15', json.dumps({k: v * 1.5 for k, v in price_kgdled_2115.items()}))

        await self._redis.hset('kgd-msw,03-2022', '8:20', json.dumps(price_kgdmsw_820))
        await self._redis.hset('kgd-msw,03-2022', '23:15', json.dumps(price_kgdmsw_2315))
        await self._redis.hset('kgd-msw,04-2022', '8:20', json.dumps({k: v * 1.5 for k, v in price_kgdmsw_820.items()}))
        await self._redis.hset('kgd-msw,04-2022', '23:15', json.dumps({k: v * 1.5 for k, v in price_kgdmsw_2315.items()}))
