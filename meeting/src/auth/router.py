import sys
sys.path.append(sys.path[0] + '/../..')
sys.path.append(sys.path[0] + '/..')

from fastapi import APIRouter

from schemas import UserCreate


user_router = APIRouter(
	prefix="/user",
	tags=["User"],
)


@user_router.post("/register")
async def register_user(user: UserCreate):
	return user