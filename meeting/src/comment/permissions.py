from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.meet.meet_service import MeetingCRUD
from src.auth.user_service import UserCRUD
from src.database import get_async_session
from src.comment.comment_service import CommentCRUD

async def is_owner_comment(
    request: Request,
    current_user_email: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    worker = CommentCRUD(session)
    comment_id = request.path_params.get("comment_id")
    user = await worker.get_user_from_comment(comment_id)

    if not user:
        raise HTTPException(status_code=403, detail="Access denied, not the comment owner")

    if current_user_email == user.email:
        return user.email
    else:
        raise HTTPException(status_code=403, detail="Access denied, not the comment owner")