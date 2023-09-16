import sys
sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4
from datetime import datetime

import pytest
from sqlalchemy import select

from tests.conftest import async_session_maker, create_users, get_participants, create_comment
from src.auth.user_service import UserCRUD
from src.auth.schemas import UserRead
from src.auth.models import User
from src.meet.models import Meeting, Participant
from src.meet.meet_service import MeetingCRUD
from src.meet.schemas import MeetingCreate
from tests.utils import is_valid_uuid
from src.comment.models import Comment
from src.comment.schemas import CommentCreate, CommentRead, CommentUpdate
from src.comment.comment_service import CommentCRUD


async def test_create_comment():
	users = await create_users(number=2)

	temp_data = {
		"place": "Odesa",
		"datetime": "2023-09-15 20:37",
		"participants": [user.email for user in users[1:]],
	}

	add_data = MeetingCreate(**temp_data)

	async with async_session_maker() as session:
		meeting_worker = MeetingCRUD(session)
		created_meeting_id = await meeting_worker.create_meeting(add_data, users[0].email)
		participant = await meeting_worker.get_participant(created_meeting_id, users[0].email)

	data = CommentCreate(comment="Hello", created_at=datetime.now())

	async with async_session_maker() as session:
		worker = CommentCRUD(session)
		created_comment_id = await worker.create_comment(created_meeting_id, users[0].email, data)

		result_comment = await session.get(Comment, created_comment_id)

		assert result_comment.participant_id == participant.id
		assert result_comment.created_at == data.created_at
		assert result_comment.comment == data.comment


async def test_read_comment():
	users = await create_users(number=2)

	temp_data = {
		"place": "Odesa",
		"datetime": "2023-09-15 20:37",
		"participants": [user.email for user in users[1:]],
	}

	add_data = MeetingCreate(**temp_data)

	async with async_session_maker() as session:
		meeting_worker = MeetingCRUD(session)
		created_meeting_id = await meeting_worker.create_meeting(add_data, users[0].email)
		participants = await meeting_worker.get_participants(created_meeting_id)

		comments = []
		for participant in participants:
			comment = Comment(
				id=uuid4(),
				participant_id=participant.id,
				created_at=datetime.now(),
				comment='hello'
			)
			session.add(comment)
			user = await session.get(User, participant.user_id)
			comments.append(CommentRead(
				id=comment.id,
				user_email=user.email,
				created_at=comment.created_at,
				comment=comment.comment)
			)

		await session.commit()

	async with async_session_maker() as session:
		worker = CommentCRUD(session)
		result_comments = await worker.read_comments(created_meeting_id)

		assert result_comments == comments


async def test_update_comment():
	comments = await create_comment()
	comment = comments[0]

	async with async_session_maker() as session:
		worker = CommentCRUD(session)
		new_data = CommentUpdate(comment="GoodBye")

		result_comment_id = await worker.update_comment(comment.id, new_data)

		result_comment = await session.get(Comment, result_comment_id)

		assert result_comment.comment == new_data.comment