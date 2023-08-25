"""add index

Revision ID: 3cf40d731db9
Revises: 691a4d717dd3
Create Date: 2023-08-25 20:29:31.865334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cf40d731db9'
down_revision: Union[str, None] = '691a4d717dd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
            CREATE INDEX idx_genre ON book(genre);
        ''')


def downgrade() -> None:
    op.execute('''
            DROP INDEX idx_genre ON book;
        ''')
