import sys

sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4, UUID

import pytest
from httpx import AsyncClient

from tests.conftest import async_session_maker
from src.config import password_hasher
from src.auth.user_service import UserCRUD


async def test_register_user(ac: AsyncClient):
	data = {
		"name": "Sasha",
		"email": "user@gmail.com",
		"last_name": "Niy",
		"password": "password1",
	}

	response = await ac.post("/user", json=data)

	async with async_session_maker() as session:
		crud = UserCRUD(session)
		user = await crud.get_user_by_email(data["email"])

		if user:
			assert type(user.id) == UUID
			assert user.name == data["name"] 
			assert user.email == data["email"]
			assert user.last_name == data["last_name"]
			assert password_hasher.verify(data["password"], user.hashed_password)
			assert user.is_active == True
			
			assert response == {
				"status": "success",
				"data": str(user.id),
				"detail": None,
			}
		else:
			assert 1 == 2

