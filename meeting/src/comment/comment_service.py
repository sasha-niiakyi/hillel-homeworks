import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID, uuid4
from typing import List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.meet.models import Meeting, Participant
from src.meet.meet_service import MeetingCRUD
from src.auth.user_service import UserCRUD
from src.auth.models import User
from src.auth.schemas import UserRead
from src.comment.models import Comment
from src.comment.schemas import CommentCreate, CommentRead, CommentUpdate


class CommentCRUD:

	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_comment(
		self, 
		meeting_id: UUID, 
		user_email: str, 
		data: CommentCreate
	) -> [UUID, None]:
		meeting_worker = MeetingCRUD(self.session)

		participant = await meeting_worker.get_participant(meeting_id, user_email)

		if participant:
			create_comment = Comment(
				id=uuid4(),
				participant_id=participant.id,
				created_at=data.created_at,
				comment=data.comment
			)

			self.session.add(create_comment)
			await self.session.commit()

			return create_comment.id

		else:
			return None

	async def read_comments(
		self, 
		meeting_id: UUID,
	) -> List[CommentRead]:
		meeting_worker = MeetingCRUD(self.session)
		user_worker = UserCRUD(self.session)

		participants = await meeting_worker.get_participants(meeting_id)

		if participants:
			result_comments = []
			for participant in participants:
				user = await user_worker.read_user(id=participant.user_id)
				query = select(Comment).where(Comment.participant_id == participant.id)
				temp_comments = await self.session.execute(query)
				comments = temp_comments.scalars().all()

				for comment in comments:
					read_comment = CommentRead(
						id=comment.id,
						user_email=user.email,
						created_at=comment.created_at,
						comment=comment.comment
					)
					result_comments.append(read_comment)

			return result_comments

		else:
			return None

	async def update_comment(
		self, 
		comment_id: UUID,
		data: CommentUpdate,
	):
		worker = CommentCRUD(self.session)
		comment = await self.session.get(Comment, comment_id)

		if comment:
			comment.comment = data.comment
			await self.session.commit()	

			return comment.id

		else:
			return None