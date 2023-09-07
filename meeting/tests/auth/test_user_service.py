import sys
sys.path.append(sys.path[0] + '/../..')

import pytest

from tests.conftest import async_session_maker
from src.auth.user_service import UserCRUD
from src.auth.models import User

async def test_create_user():
    user = User(name="John Doe", email="john@example.com", last_name='hi', hashed_password='heh')

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()

    async with async_session_maker() as session:
        saved_user = await session.get(User, user.id)
        assert saved_user.id == user.id
        assert saved_user.name == user.name
        assert saved_user.last_name == user.last_name
        assert saved_user.email == user.email
        assert saved_user.hashed_password == user.hashed_password
        assert saved_user.is_active == user.is_active
        assert saved_user == user