from uuid import uuid4
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, UUID, ForeignKey, Boolean

from src.database import Base
# from meeting import Meeting
# from src.auth.models import User


class Participant(Base):
	__tablename__ = 'participant'

	id = Column(UUID, primary_key=True ,default=uuid4())
	user_id = Column(ForeignKey('user.id'), nullable=False)
	meeting_id = Column(ForeignKey('meeting.id'), nullable=False)
	is_owner = Column(Boolean(), default=False)

	def __repr__(self) -> str:
		return f"Participant(id={self.id!r}, user={self.user_id!r}, meeting={self.meeting_id!r}, is_owner={self.is_owner!r})"

	def as_dict(self):
		return {
			"id": self.id,
			"user_id": self.user_id,
			"meeting_id": self.meeting_id,
			"is_owner": self.is_owner,
		}