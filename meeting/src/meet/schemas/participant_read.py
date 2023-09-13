import sys
from uuid import UUID
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel


class ParticipantRead(BaseModel):
	user_id: UUID
	meeting_id: UUID
	is_owner: bool

	class ConfigDict:
		'For Pydentic to convert everything to json'

		from_attributes  = True