from typing import Generator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    sessionmaker)

from app.core import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    settings.database_url)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession)


async def get_async_session() -> Generator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as async_session:
        session: AsyncSession = async_session
        yield session
