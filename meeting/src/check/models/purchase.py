from uuid import uuid4
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, UUID, ForeignKey, String, Integer
from sqlalchemy.sql import func

from src.database import Base


class Purchase(Base):
	__tablename__ = 'purchase'

	id = Column(UUID, primary_key=True ,default=uuid4())
	participant_id = Column(ForeignKey('participant.id'), nullable=False, index=True)
	order = Column(String(25), nullable=False)
	price = Column(Integer, nullable=False)

	def __repr__(self) -> str:
		return f"Purchase(id={self.id!r}, order={self.order!r}, price={self.price!r}, participant={self.participant_id!r})"