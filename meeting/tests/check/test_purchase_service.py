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
from src.meet.schemas import MeetingCreate
from tests.utils import is_valid_uuid
from src.check.models import Purchase
from src.check.purchase_service import PurchaseCRUD
from src.check.schemas import PurchaseCreate, PurchaseRead, PurchaseUpdate, PurchaseSum


async def test_create_purchase():
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
		participant = await meeting_worker.get_participant(created_meeting_id, users[0].email)

	async with async_session_maker() as session:
		worker = PurchaseCRUD(session)
		purchase_data = PurchaseCreate(order="Beer", price=300)
		created_purchase_id = await worker.create_purchase(created_meeting_id, users[0].email, purchase_data)

		purchase = await session.get(Purchase, created_purchase_id)

		assert purchase.participant_id == participant.id
		assert purchase.order == purchase_data.order
		assert purchase.price == purchase_data.price


async def test_read_purchase():
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
		participant = await meeting_worker.get_participant(created_meeting_id, users[0].email)

	async with async_session_maker() as session:
		purchases = []
		for i in range(2):
			purchase = Purchase(
				id=uuid4(), 
				participant_id=participant.id, 
				order=f"Beer{i}", 
				price=300
			)
			purchases.append(purchase)
			session.add(purchase)
		await session.commit()

		expect_result = [PurchaseRead(user_email=users[0].email, **pur.as_dict()) for pur in purchases]

		worker = PurchaseCRUD(session)
		read_purchases = await worker.read_purchases(created_meeting_id, users[0].email)

		assert read_purchases == expect_result


async def test_get_sum_for_each():
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

		participants = []

		for user in users:
			participant = await meeting_worker.get_participant(created_meeting_id, user.email)
			participants.append(participant)

	async with async_session_maker() as session:
		purchases_sum = []
		for participant in participants:
			summ = 0
			for i in range(2):
				purchase = Purchase(
					id=uuid4(), 
					participant_id=participant.id, 
					order=f"Beer{i}", 
					price=300
				)
				summ += purchase.price
				session.add(purchase)
			purchases_sum.append(summ)
		await session.commit()

		expect_result = [PurchaseSum(user_email=user.email, total=pur) for user, pur in zip(users, purchases_sum)]

		worker = PurchaseCRUD(session)
		read_total_price = await worker.get_sum_for_each(created_meeting_id)

		assert read_total_price == expect_result
