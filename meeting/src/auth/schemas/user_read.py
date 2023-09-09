from uuid import UUID
import sys
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
	id: UUID
	name: str
	last_name: str
	email: EmailStr
	is_active: bool

	class ConfigDict:
		'For Pydentic to convert everything to json'

		from_attributes  = True
