from uuid import UUID
from typing import Optional, List
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException

from src.meet.utils import datetime_validator


class MeetingUpdate(BaseModel):
	place: Optional[str] = Field(max_length=100, default=None)
	datetime: Optional[datetime_type] = None
	participants: Optional[List[EmailStr]] = []
