from uuid import UUID
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../..')
from typing import List

from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException

from src.auth.schemas import UserRead


class MeetingRead(BaseModel):
	place: str 
	datetime: datetime_type
	participants: List[UserRead]

	class Config:
		'For Pydentic to convert everything to json'

		from_attributes = True
