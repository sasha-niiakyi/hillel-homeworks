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
from src.comment.schemas import CommentCreate, CommentRead, CommentUpdate
from src.meet.permissions import is_participant
from src.comment.comment_service import CommentCRUD
from src.comment.permissions import is_owner_comment


comment_router = APIRouter(
	prefix="/meeting/comment",
	tags=["comment"],
)

@comment_router.post('/{meeting_id}')
async def create_comment(
	meeting_id: UUID,
	data: CommentCreate,
	user_email: str = Depends(is_participant),
	session: AsyncSession = Depends(get_async_session),
):
	worker = CommentCRUD(session)

	comment_id = await worker.create_comment(meeting_id, user_email, data)

	if not comment_id:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Comment wasn't created",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(comment_id),
		"detail": None,
	})

	return response


@comment_router.get('/{meeting_id}')
async def read_comment(
	meeting_id: UUID,
	user_email: str = Depends(is_participant),
	session: AsyncSession = Depends(get_async_session),
):
	worker = CommentCRUD(session)

	comments = await worker.read_comments(meeting_id)

	return comments


@comment_router.patch('/{comment_id}')
async def update_comment(
	comment_id: UUID,
	data: CommentUpdate,
	user_email: str = Depends(is_owner_comment),
	session: AsyncSession = Depends(get_async_session),
):
	worker = CommentCRUD(session)

	comment_id = await worker.update_comment(comment_id, data)

	if not comment_id:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Comment wasn't updated",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(comment_id),
		"detail": None,
	})

	return response


@comment_router.delete('/{comment_id}')
async def update_comment(
	comment_id: UUID,
	user_email: str = Depends(is_owner_comment),
	session: AsyncSession = Depends(get_async_session),
):
	worker = CommentCRUD(session)

	comment_id = await worker.delete_comment(comment_id)

	if not comment_id:
		return JSONResponse(content={
			"status": "error",
			"data": None,
			"detail": "Comment wasn't deleted",
		})

	response = JSONResponse(content={
		"status": "success",
		"data": str(comment_id),
		"detail": None,
	})

	return response