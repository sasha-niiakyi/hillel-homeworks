import sys
from uuid import UUID
sys.path.append(sys.path[0] + '/..')
from typing import Optional

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
	user_id: UUID
	meeting_id: UUID
	is_owner: Optional[bool] = False