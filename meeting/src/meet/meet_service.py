import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID, uuid4
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.meet.models import Meeting, Participant
from src.meet.schemas import MeetingCreate, MeetingRead, MeetingUpdate
from src.auth.user_service import UserCRUD
from src.auth.models import User
from src.auth.schemas import UserRead


class MeetingCRUD:

	def __init__(self, session: AsyncSession):
		self.session = session


	async def create_meeting(
		self,
		meeting: MeetingCreate,
		user_email: str,
	) -> UUID:
		create_meeting = Meeting(
			id=uuid4(),
			place=meeting.place,
			datetime=meeting.datetime #'%Y-%m-%d %H:%M'
		)

		user_worker = UserCRUD(self.session)
		current_user = await user_worker.get_user_by_email(user_email)

		create_owner = Participant(
			id=uuid4(),
			user_id=current_user.id,
			meeting_id=create_meeting.id,
			is_owner=True,
		)

		add_participants = []

		for email in meeting.participants:
			user = await user_worker.get_user_by_email(email)

			if user:
				participant = Participant(
					id=uuid4(),
					user_id=user.id,
					meeting_id=create_meeting.id,
					is_owner=False,
				)
				add_participants.append(participant)


		self.session.add(create_meeting)
		self.session.add(create_owner)

		for participant in add_participants:
			self.session.add(participant)

		await self.session.commit()
		return create_meeting.id


	async def read_meeting(self, meeting_id: UUID) -> MeetingRead:
		meeting = await self.session.get(Meeting, meeting_id)

		query = select(Participant.user_id).where(Participant.meeting_id == meeting_id)
		request_participants = await self.session.execute(query)
		users_id = request_participants.fetchall()

		participants = []
		for id in users_id:
			user = await self.session.get(User, id)
			participants.append(UserRead(**user.as_dict()))

		read_meeting = MeetingRead(
			place=meeting.place,
			datetime=meeting.datetime,
			participants=participants,
		)

		return read_meeting


	async def get_meetings(self, offset: int, limit: int = 10) -> List[Meeting]:
		if offset > 1:
			offset = (offset - 1) * limit
		else:
			offset = 0

		query = select(Meetin).offset(offset).limit(limit)
		request_meetings = await self.session.execute(query)
		meetings = request_meetings.scalars().all()

		return meetings


	async def check_participant(self, meeting_id: UUID, user_id: UUID) -> bool:
		query = select(Participant.user_id).where(Participant.meeting_id == meeting_id,
			Participant.user_id == user_id)
		return bool(await self.session.scalar(query))


	async def update_meeting(self, meeting_id: UUID, data: MeetingUpdate) -> UUID:
		meeting = await self.session.get(Meeting, meeting_id)
		user_worker = UserCRUD(self.session)

		if data.place:
			meeting.place = data.place

		if data.datetime:
			meeting.datetime = data.datetime

		if data.participants:
			for user_email in data.participants:
				user = await user_worker.get_user_by_email(user_email)
				if user:
					if not await self.check_participant(meeting_id, user.id):
						participant = Participant(
							id=uuid4(),
							user_id=user.id,
							meeting_id=meeting_id,
							is_owner=False,
						)
						self.session.add(participant)

		await self.session.commit()
		return meeting.id






		