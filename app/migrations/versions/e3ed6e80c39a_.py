"""empty message

Revision ID: e3ed6e80c39a
Revises: d205b8de8292
Create Date: 2024-04-22 00:49:48.579159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e3ed6e80c39a'
down_revision: Union[str, None] = 'd205b8de8292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('deadline', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('task', sa.Column('expired', sa.Boolean(), server_default='False', nullable=False))
    op.drop_column('task', 'Deadline')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('Deadline', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column('task', 'expired')
    op.drop_column('task', 'deadline')
    # ### end Alembic commands ###