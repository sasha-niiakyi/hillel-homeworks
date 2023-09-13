"""create_meeting_table

Revision ID: 0094203211fb
Revises: be3179af6ab9
Create Date: 2023-09-13 17:26:48.659336

"""
from uuid import uuid4
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0094203211fb'
down_revision: Union[str, None] = 'be3179af6ab9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'meeting',
        sa.Column('id', sa.UUID, primary_key=True ,default=uuid4()),
        sa.Column('place', sa.String(100), nullable=False),
        sa.Column('datetime', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
    )


def downgrade() -> None:
    op.drop_table('meeting')
