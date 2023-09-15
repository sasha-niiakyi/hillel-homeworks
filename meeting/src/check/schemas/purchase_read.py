from uuid import UUID, uuid4
import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, Field, EmailStr


class PurchaseRead(BaseModel):
	user_email: EmailStr
	order: str = Field(max_length=25)
	price: int

	class ConfigDict:
		'For Pydentic to convert everything to json'

		from_attributes = True

