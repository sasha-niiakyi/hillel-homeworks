from uuid import UUID
from typing import Optional
import sys
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import HTTPException

from utils import password_validator, name_validator


class UserCreate(BaseModel):
	name: str
	last_name: str
	email: str = Field(EmailStr, max_length=50)
	password: str
	is_active: Optional[bool]

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