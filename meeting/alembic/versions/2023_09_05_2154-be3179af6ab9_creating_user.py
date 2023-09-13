"""Creating User

Revision ID: be3179af6ab9
Revises: 
Create Date: 2023-09-05 21:54:50.410997

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be3179af6ab9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.UUID, primary_key=True ,default=uuid4()),
        sa.Column('name', sa.String(25), nullable=False),
        sa.Column('last_name', sa.String(25), nullable=False),
        sa.Column('email', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
    )


def downgrade():
    op.drop_table('user')
