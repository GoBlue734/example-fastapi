"""add content column to posts table

Revision ID: 71209006c41a
Revises: 92da39223e78
Create Date: 2023-11-14 16:14:38.599817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71209006c41a'
down_revision: Union[str, None] = '92da39223e78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')

    pass
