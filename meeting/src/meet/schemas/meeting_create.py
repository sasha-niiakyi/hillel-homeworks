from uuid import UUID
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/..')

from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException

from utils import datetime_validator


class MeetingCreate(BaseModel):
	place: str = Field(str, max_length=100)
	datetime: datetime_type

	@field_validator('datetime')
	def validate_datetime(cls, datetime: str) -> datetime_type:
		if inf := datetime_validator(datetime):
			raise HTTPException(status_code=422, detail={'status': 'error',
														'data': inf})

		return datetime_type.strptime(datetime, '%Y-%m-%d %H:%M')

