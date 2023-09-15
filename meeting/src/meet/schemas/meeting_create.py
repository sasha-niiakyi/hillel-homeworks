from uuid import UUID
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../../..')
from typing import List, Optional

from pydantic import BaseModel, field_validator, Field, EmailStr
from fastapi import HTTPException

from src.meet.utils import datetime_validator


class MeetingCreate(BaseModel):
	place: str = Field(max_length=100)
	datetime: datetime_type
	participants: Optional[List[EmailStr]] = []
