from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from config import Config

DB_URL = f"postgresql+asyncpg://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@localhost:5432/{Config.POSTGRES_DB}"

async_engine = create_async_engine(
    url = DB_URL,
    echo = True
)

async def initdb():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine, class_ = AsyncSession, expire_on_commit = False
    )

    async with async_session() as session:
        yield session


# TODO: using connection pool

import psycopg2
from sqlmodel import QueuePool

from contextlib import contextmanager

def get_conn():
    c = psycopg2.connect(user=Config.POSTGRES_USER, host=Config.POSTGRES_HOST, password=Config.POSTGRES_PASSWORD,
                         dbname=Config.POSTGRES_DB)

    return c

class PostgresqlConnectionPool(object):
    def __init__(self, pool_size = 20, max_concurrent = 40, timeout = 60):
        self.pool_size = pool_size
        if max_concurrent < 0:
            self.max_concurrent = -1
        elif max_concurrent ==0:
            self.max_concurrent = self.pool_size + 10
        else:
            self.max_concurrent = max_concurrent

        self.pool: QueuePool | None = None

        self.timeout = timeout

    @property
    def max_overflow(self):
        if self.max_concurrent < 0:
            return -1
        return self.max_concurrent - self.pool_size

    def initialize(self):
        if not self.pool:
            self.pool = QueuePool(pool_size = self.pool_size, max_overflow = self.max_overflow, timeout = self.timeout)

    @contextmanager
    def get_cursor(self):
        conn = self.pool.connect()

        try:
            yield conn.cursor()
        finally:
            conn.close()




