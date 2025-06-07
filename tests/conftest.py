import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.shared_kernel.config import config

@pytest_asyncio.fixture
async def test_session_maker():
    engine = create_async_engine(config.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield async_session
    await engine.dispose()