import sys
sys.path.append(sys.path[0] + '/../..')
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

class UserCRUD:

	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_user(
		self,
		user: User
	) -> User:
		# user = User(
		# 	name=name,
		# 	last_name=last_name,
		# 	email=email,
		# 	hashed_password=hashed_password,
		# )
		self.session.add(user)
		await self.session.flush()
		return user


	async def read_user(self, id: UUID) -> User:
		user = await self.session.query(User).get(id)
		return user


	async def update_user(self, id: UUID, **kwargs) -> User:
		user = await self.session.query(User).get(id)
		for key, value in kwargs.items():
			setattr(user, key, value)

		await self.session.flush()
		return user


	async def delete_user(self, id: UUID) -> UUID:
		user = await self.session.query(User).get(id)
		self.session.delete(user)
		await self.session.flush()
		return id


	async def get_user_by_email(self, email: str) -> User:
		user = await self.session.query(User).filter(email=email).first()
		return user


	async def check_email(self, email: str) -> bool:
		user = await self.session.query(User).filter(email=email).first()
		return bool(user)


