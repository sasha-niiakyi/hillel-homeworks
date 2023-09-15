from uuid import UUID, uuid4
import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, Field


class ParticipantRead(BaseModel):
	user_id: UUID
	meeting_id: UUID
	is_owner: bool

