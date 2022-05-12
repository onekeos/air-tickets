import os
import aioredis

from fastapi import FastAPI

from app.db.database import init_db
from app.redis.repository import RatesRepository
from app.routers.tickets import tickets_router

app = FastAPI()

app.include_router(tickets_router)

@app.on_event('startup')
async def startup():
    app.state.redis = await aioredis.from_url(f'redis://{os.getenv("REDIS_HOST")}', decode_responses=True)
    app.state.redis_repo = RatesRepository(app.state.redis)

    # todo replace with background check
    await app.state.redis_repo.load_data()
    # todo replace with alembic
    await init_db()




