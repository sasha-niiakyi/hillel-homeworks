import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID, uuid4
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead, UserUpdate, UserLogin
from src.config import password_hasher

class UserCRUD:

	def __init__(self, session: AsyncSession):
		self.session = session


	async def get_user_by_email(self, email: str) -> User:
		query = select(User).where(User.email == email)
		user = await self.session.scalar(query)
		return user


	async def create_user(
		self,
		user: UserCreate
	) -> UUID:
		create_user = User(
			id=uuid4(),
			name=user.name,
			last_name=user.last_name,
			email=user.email,
			hashed_password=password_hasher.hash(user.password),
		)
		self.session.add(create_user)
		await self.session.commit()
		return create_user.id


	async def read_user(self, id: UUID = None, user_email: str = None) -> User:
		if id:
			user = await self.session.get(User, id)

		elif user_email:
			user = await self.get_user_by_email(user_email)

		else:
			return None

		return user


	async def update_user(self, id: UUID = None, user_email: str = None, data: UserUpdate = None) -> [UUID, None]:
		if id:
			user = await self.session.get(User, id)

		elif user_email:
			user = await self.get_user_by_email(user_email)

		else:
			return None

		if user is None:
			return None

		for key, value in data.model_dump().items():
			if key == "email" and value is None:
				continue
			if hasattr(user, key):
				setattr(user, key, value)

		if data.password:
			setattr(user, "hashed_password", password_hasher.hash(data.password))

		await self.session.commit()
		return user.id


	async def delete_user(self, id: UUID = None, user_email: str = None) -> [UUID, None]:
		if id:
			user = await self.session.get(User, id)
		elif user_email:
			user = await self.get_user_by_email(user_email)
		else:
			return None

		user.is_active = False
		await self.session.commit()
		return user.id


	async def check_email(self, email: str) -> bool:
		user = await self.get_user_by_email(email)
		return bool(user)


	async def auth_user(self, user_log: UserLogin) -> bool:
		user = await self.get_user_by_email(user_log.email)
		if user:
			return password_hasher.verify(user_log.password, user.hashed_password)
		else:
			False


	async def get_users_is_active(self, offset: int, limit: int = 10) -> List[UserRead]:
		if offset > 1:
			offset = (offset - 1) * limit
		else:
			offset = 0

		query = select(User).where(User.is_active == True).offset(offset).limit(limit)
		request_users = await self.session.execute(query)
		users = request_users.scalars().all()

		result = [UserRead(**user.as_dict()) for user in users]
		
		return result

