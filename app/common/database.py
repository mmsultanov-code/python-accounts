from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from config import Config as process

DATA_BASE_URL = f"postgresql+asyncpg://{process.DB_USER}:{process.DB_PASS}@{process.DB_HOST}:{process.DB_PORT}/{process.DB_NAME}"

Base: DeclarativeMeta = declarative_base()

# import's models

import app.models.user
import app.models.role

# create engine

engine = create_async_engine(DATA_BASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# create async session

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session