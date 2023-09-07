import sys
from uuid import UUID
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
	user_id: UUID
	meeting_id: UUID