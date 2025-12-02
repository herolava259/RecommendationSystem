from sqlalchemy import text
from sqlmodel import SQLModel

from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncpg
import asyncio

POSTGRES_DB="recappdb"
POSTGRES_USER="ghostofrace"
POSTGRES_PASSWORD="1QAZ2wsx3EDC$"


DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

engine = create_async_engine(url = DB_URL, echo = True)

# "postgresql+asyncpg://ghostofrace:1QAZ2wsx3EDC$@localhost:5432/recappdb



async def test_db():
    async with engine.begin() as conn:
        statement = text("""SELECT current_user
""")
        result = await conn.execute(statement)
        print(result.all())


if __name__ == '__main__':
    asyncio.run(test_db())

    #print(SQLModel.metadata.create_all)