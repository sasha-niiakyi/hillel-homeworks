import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User
from .schemas import UserCreate, UserRead, UserUpdate
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

		for key, value in data.as_dict().items():
			if hasattr(user, key):
				setattr(user, key, value)
			else:
				return None

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

		self.session.delete(user)
		await self.session.commit()
		return id


	async def check_email(self, email: str) -> bool:
		user = await self.session.get_user_by_email(user)
		return bool(user)


