from typing import List, Optional
from uuid import uuid4
import sys, os

from sqlalchemy import String, ForeignKey, Date, UUID, Column
from sqlalchemy.sql import func

sys.path.append(sys.path[0] + '/../..')
from src.db.session import Base


class Author(Base):
	__tablename__ = 'author'

	id = Column(UUID, primary_key=True, default=uuid4())
	name = Column(String(30), nullable=False)
	fullname = Column(String(100), nullable=True)

	def __repr__(self) -> str:
		return f"Author(id={self.id!r}, name={self.name!r})"


class Book(Base):
	__tablename__ = 'book'

	id = Column(UUID, primary_key=True, default=uuid4())
	name = Column(String(30), nullable=False)
	author_id = Column(ForeignKey('author.id'))
	date_of_release = Column(Date, default=func.current_date())
	description = Column(String(300), nullable=True)
	genre = Column(String(200))

	def __repr__(self) -> str:
		return f"Book(id={self.id!r}, name={self.name!r})"
