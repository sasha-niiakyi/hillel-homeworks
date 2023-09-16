from uuid import UUID
from datetime import datetime as datetime_type
import sys
sys.path.append(sys.path[0] + '/../../..')
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException


class CommentRead(BaseModel):
	id: UUID
	user_email: EmailStr
	created_at: datetime_type
	comment: str