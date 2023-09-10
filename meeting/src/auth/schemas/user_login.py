import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import HTTPException

from src.auth.utils import password_validator


class UserLogin(BaseModel):
	email: EmailStr = Field(max_length=50)
	password: str


	@field_validator('password')
	def validate_password(cls, password: str) -> str:
		if inf := password_validator(password):
			raise HTTPException(status_code=422, detail={'status': 'error',
														'data': inf})
		return password
