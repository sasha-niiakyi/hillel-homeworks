import sys

sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4

import pytest
from httpx import AsyncClient

from tests.conftest import async_session_maker, create_test_auth_headers_for_user
from src.config import password_hasher
from src.auth.user_service import UserCRUD
from tests.utils import is_valid_uuid
from src.auth.models import User
from src.auth.schemas import UserRead


async def test_register_user(async_client: AsyncClient):
	data = {
		"name": "Sasha",
		"last_name": "Niy",
		"email": "user@gmail.com",
		"password": "password1",
	}

	response = await async_client.post("/user", json=data)

	async with async_session_maker() as session:
		crud = UserCRUD(session)
		user = await crud.get_user_by_email(data["email"])

		if user:
			assert is_valid_uuid(str(user.id))
			assert user.name == data["name"] 
			assert user.email == data["email"]
			assert user.last_name == data["last_name"]
			assert password_hasher.verify(data["password"], user.hashed_password)
			assert user.is_active == True
			
			assert response.json() == {
				"status": "success",
				"data": str(user.id),
				"detail": None,
			}
		else:
			assert False


async def test_get_user_auth(async_client: AsyncClient):
	data = {
		"name": "Sasha",
		"last_name": "Niy",
		"email": "user@gmail.com",
		"password": "password1",
	}

	user = User(
		name=data["name"],
		last_name=data["last_name"],
		email=data["email"],
		hashed_password=password_hasher.hash(data["password"]),
	)

	async with async_session_maker() as session:
		session.add(user)
		await session.commit()

	response = await async_client.get(
		f"/user/{data['email']}",
		headers=create_test_auth_headers_for_user(data["email"]),
	)
			
	assert {**response.json(), "is_active": True} == user.as_dict()


async def test_get_user_not_auth(async_client: AsyncClient):
	data = {
		"name": "Sasha",
		"last_name": "Niy",
		"email": "user@gmail.com",
		"password": "password1",
	}

	user = User(
		name=data["name"],
		last_name=data["last_name"],
		email=data["email"],
		hashed_password=password_hasher.hash(data["password"]),
	)

	async with async_session_maker() as session:
		session.add(user)
		await session.commit()

	response = await async_client.get(
		f"/user/{data['email']}",
	)
			
	assert response.json() == {"detail": "Not authenticated"}


async def test_get_user_auth_another_user(async_client: AsyncClient):
	data = {
		"name": "Sasha",
		"last_name": "Niy",
		"email": "user@gmail.com",
		"password": "password1",
	}

	user = User(
		name=data["name"],
		last_name=data["last_name"],
		email=data["email"],
		hashed_password=password_hasher.hash(data["password"]),
	)

	async with async_session_maker() as session:
		session.add(user)
		await session.commit()

	response = await async_client.get(
		f"/user/{data['email']}",
		headers=create_test_auth_headers_for_user("user@another.com"),
	)
			
	assert response.json() == {"detail": "Access denied, not the page owner"}


async def test_update_user_auth(async_client: AsyncClient):
	data = {
		"name": "Sasha",
		"last_name": "Niy",
		"email": "user@gmail.com",
		"password": "password1",
	}

	user = User(
		name=data["name"],
		last_name=data["last_name"],
		email=data["email"],
		hashed_password=password_hasher.hash(data["password"]),
	)

	new_data = {
		"name": "Sasha2",
		"last_name": "Niy2",
		"email": "user2@gmail.com",
		"password": "password2",
	}


	async with async_session_maker() as session:
		session.add(user)
		await session.commit()

	response = await async_client.patch(
		f"/user/{data['email']}",
		json=new_data,
		headers=create_test_auth_headers_for_user(data['email']),
	)

	async with async_session_maker() as session:
		crud = UserCRUD(session)
		updated_user = await crud.get_user_by_email(new_data["email"])


			
	assert is_valid_uuid(str(updated_user.id))
	assert updated_user.name == new_data["name"] 
	assert updated_user.email == new_data["email"]
	assert updated_user.last_name == new_data["last_name"]
	assert password_hasher.verify(new_data["password"], updated_user.hashed_password)
	assert updated_user.is_active == True

	assert response.json() == {
							"status": "success",
							"data": str(user.id),
							"detail": None,
							}


async def test_get_users(async_client: AsyncClient):
	list_users = []
	async with async_session_maker() as session:
		for i in range(11):
			user = User(
				id=uuid4(),
				name=f"Sasha{i}",
				email=f"user{i}@gmail.com",
				last_name=f"Niy{i}",
				hashed_password=password_hasher.hash(f"password{i}"),
			)
			list_users.append(UserRead(**user.as_dict()).as_dict())
			session.add(user)

		await session.commit()

	response = await async_client.get(
		f"/user/show/1",
		headers=create_test_auth_headers_for_user("user0@gmail.com"),
	)

	assert response.json() == list_users[:10]


