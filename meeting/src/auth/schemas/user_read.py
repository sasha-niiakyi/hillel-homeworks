from uuid import UUID
import sys
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
	name: str
	last_name: str
	email: EmailStr
	is_active: bool

	class Config:
		'For Pydentic to convert everything to json'

		from_attributes  = True
