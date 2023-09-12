from typing import AsyncGenerator
import asyncio
import sys
sys.path.append(sys.path[0] + '/..')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from httpx import AsyncClient
import pytest

from src.auth.models import User
from src.database import get_async_session
from src.main import app
from src.config import DATABASE_URL_TEST
from src.auth.jwt_utils import create_jwt_token


engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session
User.metadata.bind = engine_test

@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test", follow_redirects = True) as ac:
        yield ac


def create_test_auth_headers_for_user(email: str):
    access_token = create_jwt_token(email)
    return {"Authorization": f"Bearer {access_token}"}