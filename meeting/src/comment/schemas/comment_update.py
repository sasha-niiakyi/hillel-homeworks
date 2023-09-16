from uuid import UUID
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../../..')
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException


class CommentUpdate(BaseModel):
	comment: str = Field(max_length=500)