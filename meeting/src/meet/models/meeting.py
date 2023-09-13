from uuid import uuid4
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, String, UUID, DateTime, Boolean
from sqlalchemy.sql import func

from src.database import Base


class Meeting(Base):
	__tablename__ = 'meeting'

	id = Column(UUID, primary_key=True ,default=uuid4())
	place = Column(String, nullable=False)
	datetime = Column(DateTime, nullable=False)
	is_active = Column(Boolean(), default=True)

	def __repr__(self) -> str:
		return f"Meeting(id={self.id!r}, place={self.place!r}, datetime={self.datetime!r})"


	def as_dict(self):
		return {
			"id": self.id,
			"place": self.place,
			"datetime": self.datetime,
			"is_active": self.is_active,
		}