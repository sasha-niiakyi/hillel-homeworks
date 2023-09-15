import sys
sys.path.append(sys.path[0] + '/../../..')
sys.path.append(sys.path[0] + '/../..')
sys.path.append(sys.path[0] + '/..')
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.auth.user_service import UserCRUD
from src.database import get_async_session
from src.auth.dependencies import get_current_user, authenticate_user
from src.meet.schemas import MeetingCreate, MeetingRead, MeetingUpdate
from src.meet.meet_service import MeetingCRUD
from src.meet.permissions import is_participant
from src.check.schemas import PurchaseCreate, PurchaseRead, PurchaseSum
from src.check.models import Purchase
from src.check.purchase_service import PurchaseCRUD


purchase_router = APIRouter(
	prefix="/purchase",
	tags=["purchase"],
)

@purchase_router.post('/{meeting_id}')
async def create_purchase(
	meeting_id: UUID,
	data: PurchaseCreate,
	user_email: str = Depends(is_participant),
	session: AsyncSession = Depends(get_async_session),
):
	worker = PurchaseCRUD(session)

	purchase_id = await worker.create_purchase(meeting_id, user_email, data)

	if not purchase_id:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Purchase wasn't created",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(purchase_id),
		"detail": None,
	})

	return response


@purchase_router.get('/{meeting_id}')
async def read_own_purchases(
	meeting_id: UUID,
	user_email: str = Depends(is_participant),
	session: AsyncSession = Depends(get_async_session),
):
	worker = PurchaseCRUD(session)
	try:
		purchases = await worker.read_purchases(meeting_id, user_email)
	except:
		raise HTTPException(status_code=401,
			detail="Something was wrong")

	return purchases


@purchase_router.get('/total/{meeting_id}')
async def read_total_sum_purchases(
	meeting_id: UUID,
	user_email: str = Depends(is_participant),
	session: AsyncSession = Depends(get_async_session),
):
	worker = PurchaseCRUD(session)
	try:
		purchases = await worker.get_sum_for_each(meeting_id)
	except:
		raise HTTPException(status_code=401,
			detail="Something was wrong")

	return purchases