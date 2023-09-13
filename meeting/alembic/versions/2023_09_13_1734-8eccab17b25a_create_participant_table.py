"""create_participant_table

Revision ID: 8eccab17b25a
Revises: 0094203211fb
Create Date: 2023-09-13 17:34:56.233064

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eccab17b25a'
down_revision: Union[str, None] = '0094203211fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'participant',
        sa.Column('id', sa.UUID, primary_key=True ,default=uuid4()),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('meeting_id', sa.UUID, sa.ForeignKey('meeting.id'), nullable=False),
        sa.Column('is_owner', sa.Boolean(), default=False),
    )


def downgrade() -> None:
    op.drop_table('participant')
