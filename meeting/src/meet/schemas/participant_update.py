import sys
from uuid import UUID
from typing import Optional
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel


class ParticipantUpdate(BaseModel):
	user_id: UUID
	meeting_id: UUID
