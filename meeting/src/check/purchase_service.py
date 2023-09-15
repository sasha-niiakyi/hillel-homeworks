import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID, uuid4
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.meet.models import Meeting, Participant
from src.meet.meet_service import MeetingCRUD
from src.auth.user_service import UserCRUD
from src.auth.models import User
from src.auth.schemas import UserRead
from src.check.schemas import PurchaseCreate, PurchaseRead, PurchaseSum
from src.check.models import Purchase


class PurchaseCRUD:

	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_purchase(
		self, 
		meeting_id: UUID, 
		user_email: str, 
		data: PurchaseCreate
	) -> [UUID, None]:
		meeting_worker = MeetingCRUD(self.session)

		participant = await meeting_worker.get_participant(meeting_id, user_email)

		if participant:
			create_purchase = Purchase(
				id=uuid4(),
				participant_id=participant.id,
				**data.model_dump(),
			)

			self.session.add(create_purchase)
			await self.session.commit()

			return create_purchase.id

		else:
			return None


	async def read_purchases(
		self, 
		meeting_id: UUID, 
		user_email: str, 
	) -> List[PurchaseRead]:
		meeting_worker = MeetingCRUD(self.session)

		participant = await meeting_worker.get_participant(meeting_id, user_email)

		if participant:
			query = select(Purchase).where(Purchase.participant_id == participant.id)
			request_purchases = await self.session.execute(query)
			purchases = request_purchases.scalars().all()

			if not purchases:
				return []

			read_purchases = []
			for purchase in purchases:
				read_purchase = PurchaseRead(
					user_email=user_email,
					order=purchase.order,
					price=purchase.price,
				)
				read_purchases.append(read_purchase)

			return read_purchases

		else:
			return None


	async def get_sum_for_each(
		self, 
		meeting_id: UUID,
	) -> List[PurchaseSum]:
		meeting_worker = MeetingCRUD(self.session)

		meeting = await meeting_worker.read_meeting(meeting_id)

		if meeting:
			each = []
			for user in meeting.participants:
				purchases = await self.read_purchases(meeting_id, user.email)
				if purchases:
					list_sum = [purchase.price for purchase in purchases]

					each.append(PurchaseSum(user_email=user.email, total=sum(list_sum)))
				else:
					each.append(PurchaseSum(user_email=user.email, total=0))

			return each

		else:
			return None


