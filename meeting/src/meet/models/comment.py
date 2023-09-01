from uuid import uuid4
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, UUID, ForeignKey, DateTime, String
from sqlalchemy.sql import func

from src.models import Base


class Comment(Base):
	__tablename__ = 'comment'

	id = Column(UUID, primary_key=True ,default=uuid4())
	participant_id = Column(ForeignKey('participant.id'), nullable=False)
	created_at = Column(DateTime, default=func.current_timestamp())
	comment = Column(String(500), nullable=False)

	def __repr__(self) -> str:
		return f"Comment(id={self.id!r}, created_at={self.created_at!r}, comment={self.comment[:15]!r}, participant={self.participant_id!r})"