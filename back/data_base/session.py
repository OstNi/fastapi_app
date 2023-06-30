from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Generator
import setting

# создание engine для взаимодействия с бд
engine = create_async_engine(setting.DATABASE_URL, future=True, echo=True)

# создание сессии для взаимодействия с бд
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
