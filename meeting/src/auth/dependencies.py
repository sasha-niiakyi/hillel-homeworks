import jwt
from typing import Union
import sys
sys.path.append(sys.path[0] + '/../..')

from fastapi import Depends, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.user_service import UserCRUD
from src.database import get_async_session
from src.config import password_hasher
from src.auth.models import User
from src.auth.jwt_utils import decode_jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> Union[User, None]:
    crud = UserCRUD(session)
    user = await crud.get_user_by_email(email)

    if user is None:
        return None
    if not password_hasher.verify(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_jwt_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise exception
    except:
        raise exception

    return email