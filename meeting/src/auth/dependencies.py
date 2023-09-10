from jwt import PyJWTError, decode
from typing import Optional
import sys
sys.path.append(sys.path[0] + '/../..')

from fastapi import Depends, HTTPException, Request, Cookie

from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("token")
        if token is None:
            return None

        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        return email

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")