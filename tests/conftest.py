import os
from typing import AsyncGenerator
import asyncio

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
import pytest
import pytest_asyncio
from httpx import AsyncClient

from db import get_async_session
from models import Base
from main import app


load_dotenv()

DB_TEST_DSN = os.environ.get("DATABASE_TEST_DSN")

engine_test = create_async_engine(DB_TEST_DSN, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():

    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


client = TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
