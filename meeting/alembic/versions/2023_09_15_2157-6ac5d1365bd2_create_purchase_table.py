"""create_purchase_table

Revision ID: 6ac5d1365bd2
Revises: 8eccab17b25a
Create Date: 2023-09-15 21:57:52.915683

"""
from uuid import uuid4
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ac5d1365bd2'
down_revision: Union[str, None] = '8eccab17b25a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'purchase',
        sa.Column('id', sa.UUID, primary_key=True ,default=uuid4()),
        sa.Column('participant_id', sa.UUID, sa.ForeignKey('participant.id'), nullable=False),
        sa.Column('order', sa.String(25), nullable=False),
        sa.Column('price', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('purchase')
