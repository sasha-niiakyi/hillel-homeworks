import sys
sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4, UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from tests.conftest import async_session_maker, create_test_auth_headers_for_user
from tests.conftest import create_users, get_participants, get_expect_participants
from src.config import password_hasher
from src.auth.user_service import UserCRUD
from tests.utils import is_valid_uuid
from src.auth.models import User
from src.auth.schemas import UserRead
from src.meet.models import Meeting
from src.meet.schemas import MeetingCreate, MeetingRead, MeetingUpdate
from src.meet.meet_service import MeetingCRUD


async def test_create_meeting_auth(async_client: AsyncClient):
	users = await create_users(number=2)

	data = {
		"place": "Odesa",
		"datetime": "2023-09-15 07:37",
		"participants": [user.email for user in users[1:]],
	}

	expect_data = MeetingCreate(**data)

	response = await async_client.post(
		"/meetings",
		json=data,
		headers=create_test_auth_headers_for_user(users[0].email),
	)

	async with async_session_maker() as session:
		response = response.json()
		assert response["status"] == "success"
		assert is_valid_uuid(response["data"])
		assert response["detail"] is None

		if is_valid_uuid(response["data"]):
			meeting_id = response["data"]

			saved_meeting = await session.get(Meeting, meeting_id)
			result_participants = await get_participants(meeting_id)

			expect_participants = await get_expect_participants(meeting_id, users)

			assert result_participants == expect_participants
			assert saved_meeting.place == expect_data.place
			assert saved_meeting.datetime == expect_data.datetime
			assert saved_meeting.is_active == True
		else:
			assert False


async def test_create_meeting_not_auth(async_client: AsyncClient):
	data = {
		"place": "Odesa",
		"datetime": "2023-09-15 07:37",
		"participants": [],
	}

	response = await async_client.post(
		"/meetings",
		json=data,
	)

	assert response.json() == {"detail": "Not authenticated"}


async def test_read_meeting_auth(async_client: AsyncClient):
	users = await create_users(number=2)

	data = {
		"place": "Odesa",
		"datetime": "2023-09-15 20:37",
		"participants": [user.email for user in users[1:]],
	}

	expect_data = MeetingCreate(**data)

	async with async_session_maker() as session:
		meeting_worker = MeetingCRUD(session)
		created_meeting_id = await meeting_worker.create_meeting(expect_data, users[0].email)

	response = await async_client.get(
		f"/meetings/{created_meeting_id}",
		headers=create_test_auth_headers_for_user(users[0].email),
	)

	async with async_session_maker() as session:
		response = response.json()

		participants = [UserRead(**user.as_dict()).as_dict() for user in users]

		# expect_result = MeetingRead(
		# 	place=expect_data.place,
		# 	datetime=expect_data.datetime,
		# 	participants=participants,
		# )

		expect_result = {
			"place": expect_data.place,
			"datetime": (data["datetime"].replace(' ', 'T') + ':00'),
			"participants": participants
		}

		assert response == expect_result