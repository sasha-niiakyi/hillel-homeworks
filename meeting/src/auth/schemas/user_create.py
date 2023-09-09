from uuid import UUID, uuid4
from typing import Optional
import sys
sys.path.append(sys.path[0] + '/../..')
import json

from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import HTTPException

from src.auth.utils import password_validator, name_validator


class UserCreate(BaseModel):
	name: str
	last_name: str
	email: EmailStr = Field(max_length=50)
	password: str
	is_active: Optional[bool] = True

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
			"is_active": self.is_active,
		}
		return user_data