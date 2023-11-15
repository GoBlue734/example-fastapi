"""Create posts table

Revision ID: 92da39223e78
Revises: 
Create Date: 2023-11-14 14:42:16.633332

"""
from typing import Sequence, Union#Sequence is used to specify the type of a list. Union is used to specify the type of a variable.

from alembic import op#The op object is used to perform operations on the database.
import sqlalchemy as sa#The sa object is used to perform operations on the database.


# revision identifiers, used by Alembic.
revision: str = '92da39223e78'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


#Handles the changes to be made to the database schema.
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(length=255), nullable=False))

    pass

#Handles the reversal of the changes made to the database schema.
def downgrade() -> None:
    op.drop_table('posts')

    pass
