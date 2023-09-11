import sys
sys.path.append(sys.path[0] + '/../..')
sys.path.append(sys.path[0] + '/..')

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import UserCreate, UserLogin, UserRead, Token, UserUpdate
from src.auth.user_service import UserCRUD
from src.database import get_async_session
from src.auth.jwt_utils import create_jwt_token
from src.auth.dependencies import get_current_user, authenticate_user
from src.auth.permissions import is_owner


user_router = APIRouter(
	prefix="/user",
	tags=["user"],
)

login_router = APIRouter(
	prefix="/login",
	tags=["login"],
)

@login_router.post("/token", response_model=Token)
async def login_for_access_token(
	form_data: OAuth2PasswordRequestForm = Depends(),
	session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401,
            detail="Incorrect username or password")
    access_token = create_jwt_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/")
async def register_user(
	user: UserCreate,
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

	response = JSONResponse(content={
		"status": "success",
		"data": str(created_user),
		"detail": None,
	})

	return response


@user_router.get("/{user_email}", response_model=UserRead)
async def home_user(
	user_email: str,
	is_owner: bool = Depends(is_owner),
	session: AsyncSession = Depends(get_async_session)
):
	crud = UserCRUD(session)
	user = await crud.get_user_by_email(user_email)

	response = UserRead(**user.as_dict())
	return response


@user_router.patch('/{user_email}')
async def update_user(
	user_email: str,
	data: UserUpdate,
	is_owner: bool = Depends(is_owner),
	session: AsyncSession = Depends(get_async_session)
):
	crud = UserCRUD(session)
	updated_user = await crud.update_user(user_email=user_email, data=data)
	response = JSONResponse(content={
		"status": "success",
		"data": str(updated_user),
		"detail": None,
	})
	return response


@user_router.delete('/{user_email}')
async def delete_user(
	user_email: str,
	is_owner: bool = Depends(is_owner),
	session: AsyncSession = Depends(get_async_session)
):
	crud = UserCRUD(session)
	updated_user = await crud.delete_user(user_email=user_email)
	response = JSONResponse(content={
		"status": "success",
		"data": str(updated_user),
		"detail": None,
	})
	return response