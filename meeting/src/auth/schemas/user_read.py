from uuid import UUID
import sys
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
	id: UUID
	name: str
	last_name: str
	email: EmailStr

	class ConfigDict:
		'For Pydentic to convert everything to json'

		from_attributes  = True

	def as_dict(self):
		user_data = {
			"id": str(self.id),
			"name": self.name,
			"last_name": self.last_name,
			"email": self.email,
		}
		return user_data
