import sys
sys.path.append(sys.path[0] + '/../..')
sys.path.append(sys.path[0] + '/..')

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.auth.schemas import UserCreate, UserLogin
from src.auth.user_service import UserCRUD
from src.database import get_async_session
from src.auth.jwt_utils import create_jwt_token
from src.auth.dependencies import get_current_user


user_router = APIRouter(
	prefix="/user",
	tags=["User"],
)

@user_router.post("/register")
async def register_user(user: UserCreate,
	session: AsyncSession = Depends(get_async_session)
):
	user_crud = UserCRUD(session)

	if await user_crud.check_email(user.email):
		raise HTTPException(status_code=422, detail={
			"status": "error",
			"data": None,
			"detail": "Email already exists",
		})

	created_user = await user_crud.create_user(user)

	token = create_jwt_token(user.email)
	response = JSONResponse(content={
		"status": "success",
		"data": str(created_user),
		"detail": None,
	})
	response.set_cookie("token", token)

	return response


@user_router.post("/login")
async def login_user(user_log: UserLogin,
	session: AsyncSession = Depends(get_async_session)
):
	user_crud = UserCRUD(session)

	if await user_crud.auth_user(user_log):
		token = create_jwt_token(user_log.email)

		response = JSONResponse(content={
			"status": "success",
			"data": user_log.email,
			"detail": None,
		})
		response.set_cookie("token", token)

		return response

	else:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"detail": "Email or password isn`t corrected",
		})


@user_router.get("/{user_email}")
async def login_user(user_email: str,
	current_user: str = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session)
):
	if current_user == user_email:
		return current_user
	else:
		return "Wrong"
