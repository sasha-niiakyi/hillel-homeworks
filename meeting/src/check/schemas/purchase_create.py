from uuid import UUID, uuid4
import sys
sys.path.append(sys.path[0] + '/../..')

from pydantic import BaseModel, Field


class PurchaseCreate(BaseModel):
	order: str = Field(max_length=25)
	price: int

