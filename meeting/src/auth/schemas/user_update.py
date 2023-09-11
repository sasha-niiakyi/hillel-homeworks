from uuid import UUID
from typing import Optional
import sys
sys.path.append(sys.path[0] + '/..')
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, EmailStr, field_validator, Field

from src.auth.utils import password_validator, name_validator


class UserUpdate(BaseModel):
	name: Optional[str] = None
	last_name: Optional[str] = None
	email: Optional[EmailStr] = Field(max_length=50, default=None)
	password: Optional[str] = None

	@field_validator('name')
	def validate_name(cls, name: str) -> str:
		if inf := name_validator(name):
			raise HTTPException(status_code=422, detail={'status': 'error',
														'data': inf})
		return name

	@field_validator('password')
	def validate_password(cls, password: str) -> str:
		if inf := password_validator(password):
			raise HTTPException(status_code=422, detail={'status': 'error',
														'data': inf})
		return password

	def as_dict(self):
		user_data = {
			"name": self.name,
			"last_name": self.last_name,
			"email": self.email,
		}
		return user_data
