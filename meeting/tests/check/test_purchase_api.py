import sys
sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4, UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from tests.conftest import async_session_maker, create_test_auth_headers_for_user, create_ump
from tests.conftest import create_users, get_participants, get_expect_participants
from src.config import password_hasher
from src.auth.user_service import UserCRUD
from tests.utils import is_valid_uuid
from src.auth.models import User
from src.meet.models import Meeting
from src.meet.meet_service import MeetingCRUD
from src.check.models import Purchase



async def test_create_purchase_auth(async_client: AsyncClient):
	user, meeting, participant = await create_ump()

	data = {
		"order": "Pepsi",
		"price": 400,
	}

	response = await async_client.post(
		f"/purchase/{meeting.id}",
		json=data,
		headers=create_test_auth_headers_for_user(user.email),
	)

	async with async_session_maker() as session:
		query = select(Purchase).where(Purchase.participant_id == participant.id)
		temp_purchase = await session.execute(query)
		purchase = temp_purchase.scalar()

		expect_response = {
			"status": "success",
			"data": str(purchase.id),
			"detail": None,
		}

		assert response.json() == expect_response
		assert purchase.participant_id == participant.id
		assert purchase.order == data["order"]
		assert purchase.price == data["price"]


async def test_create_purchase_not_auth(async_client: AsyncClient):
	user, meeting, participant = await create_ump()

	data = {
		"order": "Pepsi",
		"price": 400,
	}

	response = await async_client.post(
		f"/purchase/{meeting.id}",
		json=data,
	)

	assert response.json() == {"detail": "Not authenticated"}

	async with async_session_maker() as session:
		query = select(Purchase)
		temp_purchase = await session.execute(query)
		purchase = temp_purchase.scalar()

		assert purchase is None


async def test_create_purchase_not_join(async_client: AsyncClient):
	user, meeting, participant = await create_ump()

	async with async_session_maker() as session:
		user2 = User(
			id=uuid4(),
			name="Sasha2",
			last_name="Niy2",
			email="user2@gmail.com",
			hashed_password=password_hasher.hash("password2"),
		)
		session.add(user)
		await session.commit()

	data = {
		"order": "Pepsi",
		"price": 400,
	}

	response = await async_client.post(
		f"/purchase/{meeting.id}",
		json=data,
		headers=create_test_auth_headers_for_user(user2.email),
	)

	assert response.json() == {"detail": "Access denied, not join to the meeting"}

	async with async_session_maker() as session:
		query = select(Purchase)
		temp_purchase = await session.execute(query)
		purchase = temp_purchase.scalar()

		assert purchase is None


async def test_read_purchase_auth(async_client: AsyncClient):
	user, meeting, participant = await create_ump()

	data = {
		"order": "Pepsi",
		"price": 400,
	}
	async with async_session_maker() as session:
		purchase = Purchase(
			id=uuid4(),
			participant_id=participant.id,
			order=data["order"],
			price=data["price"],
		)
		session.add(purchase)
		await session.commit()


	response = await async_client.get(
		f"/purchase/{meeting.id}",
		headers=create_test_auth_headers_for_user(user.email),
	)

	expect_response = [
		{
			"user_email": user.email,
			"order": purchase.order,
			"price": purchase.price
		}
	]

	assert response.json() == expect_response
