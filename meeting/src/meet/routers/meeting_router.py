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
from src.meet.permissions import is_owner_meeting


meet_router = APIRouter(
	prefix="/meetings",
	tags=["meeting"],
)

@meet_router.post("/")
async def create_meeting(
	meeting: MeetingCreate,
	user_email: str = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session),
):
	worker = MeetingCRUD(session)

	meeting_id = await worker.create_meeting(meeting, user_email)

	response = JSONResponse(content={
		"status": "success",
		"data": str(meeting_id),
		"detail": None,
	})

	return response


@meet_router.get("/{meeting_id}", response_model=MeetingRead)
async def read_meeting(
	meeting_id: UUID,
	user_email: str = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session),
):
	worker = MeetingCRUD(session)

	meeting = await worker.read_meeting(meeting_id)

	if not meeting:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Meeting wasn't found",
		})

	return meeting


@meet_router.get("/show/{page}")
async def show_meetings(
	page: int,
	user_email: str = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session),
):
	worker = MeetingCRUD(session)

	meetings = await worker.get_meetings(offset=page)

	# response = JSONResponse(content={
	# 	"status": "success",
	# 	"data": meetings,
	# 	"detail": None,
	# })

	return meetings


@meet_router.patch("/join/{meeting_id}")
async def join_meeting(
	meeting_id: UUID,
	user_email: str = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session),
):
	worker = MeetingCRUD(session)

	data = MeetingUpdate(
		place=None,
		datetime=None,
		participants=[user_email],
	)

	meeting = await worker.update_meeting(meeting_id, data)

	if not meeting:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Meeting wasn't found",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(meeting_id),
		"detail": None,
	})

	return response


@meet_router.patch("/{meeting_id}")
async def update_meeting(
	meeting_id: UUID,
	data: MeetingUpdate,
	is_owner: bool = Depends(is_owner_meeting),
	session: AsyncSession = Depends(get_async_session),
):
	worker = MeetingCRUD(session)

	meeting = await worker.update_meeting(meeting_id, data)

	if not meeting:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Meeting wasn't found",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(meeting_id),
		"detail": None,
	})

	return response