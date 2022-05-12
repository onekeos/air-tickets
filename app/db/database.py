import os
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = os.getenv("POSTGRES_USER", 'postgres')
PASS = os.getenv("POSTGRES_PASSWORD", 'pass')
HOST = os.getenv("POSTGRES_HOST", 'db')
PORT = os.getenv("POSTGRES_PORT", '5432')
DB_NAME = os.getenv("POSTGRES_DB", 'postgres')

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASS}@{HOST}/{DB_NAME}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("""CREATE SCHEMA IF NOT EXISTS ticket;"""))
    await engine.dispose()
