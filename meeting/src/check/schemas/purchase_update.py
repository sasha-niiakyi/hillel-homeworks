from uuid import UUID, uuid4
import sys
from typing import Optional
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, Field, EmailStr


class PurchaseUpdate(BaseModel):
	order: Optional[str] = Field(max_length=25, default=None)
	price: Optional[int] = None
