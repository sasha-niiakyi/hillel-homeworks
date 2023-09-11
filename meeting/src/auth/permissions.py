from fastapi import Request, Depends, HTTPException
from src.auth.dependencies import get_current_user

async def is_owner(request: Request, current_user_email: str = Depends(get_current_user)):
    user_email = request.path_params.get("user_email")
    if user_email == current_user_email:
        return True
    else:
        raise HTTPException(status_code=403, detail="Access denied, not the page owner")