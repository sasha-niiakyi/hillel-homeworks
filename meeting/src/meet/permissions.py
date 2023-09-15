from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.meet.meet_service import MeetingCRUD
from src.auth.user_service import UserCRUD
from src.database import get_async_session

async def is_owner_meeting(
    request: Request,
    current_user_email: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    worker = MeetingCRUD(session)

    meeting_id = request.path_params.get("meeting_id")
    participant = await worker.get_participant(meeting_id, current_user_email)

    if participant.is_owner:
        return True
    else:
        raise HTTPException(status_code=403, detail="Access denied, not the page owner")


async def is_participant(
    request: Request,
    current_user_email: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    worker = MeetingCRUD(session)

    meeting_id = request.path_params.get("meeting_id")
    participant = await worker.get_participant(meeting_id, current_user_email)

    if participant:
        return current_user_email
    else:
        raise HTTPException(status_code=403, detail="Access denied, not join to the meeting")