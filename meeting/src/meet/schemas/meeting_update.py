from uuid import UUID
from typing import Optional
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException

from src.meet.utils import datetime_validator


class MeetingUpdate(BaseModel):
	place: Optional[str] = Field(max_length=100, default=None)
	datetime: Optional[datetime_type]

	@field_validator('datetime')
	def validate_datetime(cls, datetime: str) -> datetime_type:
		if inf := datetime_validator(datetime):
			raise HTTPException(status_code=422, detail={'status': 'error',
														'data': inf})

		return datetime_type.strptime(datetime, '%Y-%m-%d %H:%M')