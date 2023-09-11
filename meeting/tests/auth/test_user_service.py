import sys

sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4

import pytest

from tests.conftest import async_session_maker
from src.config import password_hasher
from src.auth.user_service import UserCRUD
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate


async def test_create_user():
    user = UserCreate(
        name="Sasha",
        email="shlyapa@example.com",
        last_name="Niy",
        password="password1",
    )

    async with async_session_maker() as session:
        crud = UserCRUD(session)
        user_id = await crud.create_user(user)

        saved_user = await session.get(User, user_id)
        expect_result = {**{"id": str(user_id)}, **user.as_dict(), "is_active": True}

        assert password_hasher.verify(user.password, saved_user.hashed_password)
        assert saved_user.as_dict() == expect_result


@pytest.mark.parametrize(
    "field",
    [
        ("id",),
        ("email",),
        ("test",),
    ],
)
async def test_read_user(field):
    user = User(
        name="Sasha",
        email="shlyapa@example.com",
        last_name="Niy",
        hashed_password=password_hasher.hash("password1"),
    )

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()

    async with async_session_maker() as session:
        crud = UserCRUD(session)

        if field == "id":
            read_user = await crud.read_user(id=user.id)

            assert password_hasher.verify("password1", read_user.hashed_password)
            assert read_user.as_dict == user.as_dict

        elif field == "email":
            read_user = await crud.read_user(email=user.id)

            assert password_hasher.verify("password1", read_user.hashed_password)
            assert read_user.as_dict == user.as_dict

        elif field == "test":
            read_user = await crud.read_user(email=user.id)

            assert read_user == None


@pytest.mark.parametrize(
    "field, update_data, result_data",
    [
        (
            "id",
            {
                "name": "Sasha2",
                "email": "shlyapa2@example.com",
                "last_name": "Niy2",
                "password": "password2",
            },
            {
                "id": "f61b3a2b-d6dd-4c73-9c23-da0bce0fe133",
                "name": "Sasha2",
                "email": "shlyapa2@example.com",
                "last_name": "Niy2",
            },
        ),
        (
            "email",
            {
                "name": "Sasha2",
                "email": "shlyapa2@example.com",
                "last_name": "Niy2",
                "password": "password2",
            },
            {
                "id": "f61b3a2b-d6dd-4c73-9c23-da0bce0fe133",
                "name": "Sasha2",
                "email": "shlyapa2@example.com",
                "last_name": "Niy2",
            },
        ),
    ],
)
async def test_update_user(field, update_data, result_data):
    user = User(
        id="f61b3a2b-d6dd-4c73-9c23-da0bce0fe133",
        name="Sasha",
        email="shlyapa@example.com",
        last_name="Niy",
        hashed_password=password_hasher.hash("password1"),
    )

    new_user_data = UserUpdate(
        **update_data
    )

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()

    async with async_session_maker() as session:
        crud = UserCRUD(session)

        if field == "id":
            up_user_id = await crud.update_user(id=user.id, data=new_user_data)

            updated_user = await session.get(User, user.id)

            result_data = {**{"id": str(user.id)}, **new_user_data.as_dict(), "is_active": True}

            assert password_hasher.verify(new_user_data.password, updated_user.hashed_password)
            assert updated_user.as_dict() == result_data

        elif field == "email":
            up_user_id = await crud.update_user(user_email=user.email, data=new_user_data)

            updated_user = await session.get(User, user.id)

            result_data = {**{"id": str(user.id)}, **new_user_data.as_dict(), "is_active": True}

            assert password_hasher.verify(new_user_data.password, updated_user.hashed_password)
            assert updated_user.as_dict() == result_data



@pytest.mark.parametrize(
    "field",
    [
        ("id",),
        ("email",),
    ],
)
async def test_delete_user(field):
    user = User(
        id="be60e58d-99c8-4ec0-92e3-c1861e3e63f5",
        name="Sasha3",
        email="shlyapa3@example.com",
        last_name="Niy3",
        hashed_password="password43",
    )

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()

    async with async_session_maker() as session:
        crud = UserCRUD(session)
        if field == "id":
            deleted_user = await crud.delete_user(id=user.id)

            result = await session.get(User, user.id)
            assert result.is_active == False
            assert deleted_user == user.id

        elif field == "email":
            deleted_user = await crud.delete_user(user_email=user.email)

            result = await session.get(User, user.email)
            assert result.is_active == False
            assert deleted_user == user.id
