"""create_comment_table

Revision ID: 6bc28cab3972
Revises: 6ac5d1365bd2
Create Date: 2023-09-16 14:16:08.564839

"""
from uuid import uuid4
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bc28cab3972'
down_revision: Union[str, None] = '6ac5d1365bd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'comment',
        sa.Column('id', sa.UUID, primary_key=True ,default=uuid4()),
        sa.Column('participant_id', sa.UUID, sa.ForeignKey('participant.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('comment', sa.String(500), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('comment')