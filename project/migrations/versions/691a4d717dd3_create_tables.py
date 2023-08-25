"""create tables

Revision ID: 691a4d717dd3
Revises: 
Create Date: 2023-08-25 20:08:34.262158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '691a4d717dd3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
            CREATE TABLE author (
                id UUID PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                fullname VARCHAR(100)
            )
        ''')

    op.execute('''
            CREATE TABLE book (
                id UUID PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                author UUID REFERENCES author(id),
                date_of_release DATE DEFAULT CURRENT_DATE,
                desctiption VARCHAR(300),
                genre VARCHAR(200) NOT NULL
            )
        ''')


def downgrade() -> None:
    op.drop_table('book')
    op.drop_table('author')
