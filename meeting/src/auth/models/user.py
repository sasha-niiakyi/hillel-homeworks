from uuid import uuid4
import json
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, String, UUID, Boolean

from src.database import Base


class User(Base):
	__tablename__ = 'user'

	id = Column(UUID, primary_key=True ,default=uuid4())
	name = Column(String(25), nullable=False)
	last_name = Column(String(25), nullable=False)
	email = Column(String(50), unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean(), default=True) # it`ll be checked later

	def __repr__(self) -> str:
		return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

	def convert_json(self):
		user_data = {
			"id": str(self.id),
			"name": self.name,
			"last_name": self.last_name,
			"email": self.email,
			"is_active": self.is_active,
		}
		return json.dumps(user_data)

	def as_dict(self):
		user_data = {
			"id": str(self.id),
			"name": self.name,
			"last_name": self.last_name,
			"email": self.email,
			"is_active": self.is_active,
		}
		return user_data