import sys
sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4

import pytest
from sqlalchemy import select

from tests.conftest import async_session_maker, create_users, get_participants
from src.auth.user_service import UserCRUD
from src.auth.schemas import UserRead
from src.auth.models import User
from src.meet.models import Meeting, Participant
from src.meet.meet_service import MeetingCRUD
from src.meet.schemas import MeetingCreate, MeetingRead, MeetingUpdate
from tests.utils import is_valid_uuid
from src.config import password_hasher


async def test_create_meeting():
	users = await create_users(number=3)

	meeting = MeetingCreate(
		place="Odesa",
		datetime="2023-09-17 17:30",
		participants=[users[1].email, users[2].email],
	)

	async with async_session_maker() as session:
		worker = MeetingCRUD(session)
		meeting_id = await worker.create_meeting(meeting, users[0].email)

		saved_meeting = await session.get(Meeting, meeting_id)
		result_participants = await get_participants(meeting_id)

		expect_participants = []
		for user in users:
			if user.id == users[0].id:
				expect_participants.append({
						"user_id": user.id,
						"meeting_id": meeting_id,
						"is_owner": True
					}
				)
			else:
				expect_participants.append({
						"user_id": user.id,
						"meeting_id": meeting_id,
						"is_owner": False
					}
				)


		expect_result = []

		assert result_participants == expect_participants
		assert is_valid_uuid(str(saved_meeting.id))
		assert saved_meeting.place == meeting.place
		assert saved_meeting.datetime == meeting.datetime
		assert saved_meeting.is_active == True


async def test_read_meeting():
	users = await create_users(number=3)

	async with async_session_maker() as session:
		meet_schema = MeetingCreate(
			place="Odesa",
			datetime="2023-09-17 17:30",
			participants=[users[1].email, users[2].email],
		)

		created_meeting = Meeting(
			id=uuid4(),
			place=meet_schema.place,
			datetime=meet_schema.datetime #'%Y-%m-%d %H:%M'
		)

		user_worker = UserCRUD(session)
		current_user = await user_worker.get_user_by_email(users[0].email)

		participants = []

		create_owner = Participant(
			id=uuid4(),
			user_id=current_user.id,
			meeting_id=created_meeting.id,
			is_owner=True,
		)

		session.add(created_meeting)
		session.add(create_owner)

		participants.append(UserRead(**current_user.as_dict()))

		for user in users[1:]:
			participant = Participant(
				id=uuid4(),
				user_id=user.id,
				meeting_id=created_meeting.id,
				is_owner=False,
			)
			session.add(participant)
			participants.append(UserRead(**user.as_dict()))

		await session.commit()

		expect_result = MeetingRead(
			place=created_meeting.place,
			datetime=created_meeting.datetime,
			participants=participants,
		)

	async with async_session_maker() as session:
		worker = MeetingCRUD(session)
		result = await worker.read_meeting(created_meeting.id)

		assert result.model_dump() == expect_result.model_dump()


async def test_update_meeting():
	users = await create_users(number=2)

	async with async_session_maker() as session:
		meet_schema = MeetingCreate(
			place="Odesa",
			datetime="2023-09-17 17:30",
			participants=[],
		)

		meeting = Meeting(
			id=uuid4(),
			place=meet_schema.place,
			datetime=meet_schema.datetime #'%Y-%m-%d %H:%M'
		)

		create_owner = Participant(
			id=uuid4(),
			user_id=users[0].id,
			meeting_id=meeting.id,
			is_owner=True,
		)

		session.add(meeting)
		session.add(create_owner)
		await session.commit()


		update_data = {
			"place": "Kyiv",
			"datetime": "2023-09-20 20:00",
			"participants": [users[1].email],
		}

		new_data = MeetingUpdate(
			**update_data
		)

		worker = MeetingCRUD(session)
		updated_id = await worker.update_meeting(meeting.id, new_data)


		updated_meeting = await session.get(Meeting, meeting.id)
		result_participants = await get_participants(meeting.id)

		expect_participants = []
		for user in users:
			if user.id == users[0].id:
				expect_participants.append({
						"user_id": user.id,
						"meeting_id": meeting.id,
						"is_owner": True
					}
				)
			else:
				expect_participants.append({
						"user_id": user.id,
						"meeting_id": meeting.id,
						"is_owner": False
					}
				)


		assert updated_id == meeting.id
		assert result_participants == expect_participants
		assert updated_meeting.place == new_data.place
		assert updated_meeting.datetime == new_data.datetime
		assert updated_meeting.is_active == True

		