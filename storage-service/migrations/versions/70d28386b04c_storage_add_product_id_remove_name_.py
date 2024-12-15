"""storage: Add product_id, remove name, price, description

Revision ID: 70d28386b04c
Revises: c28d1aae0099
Create Date: 2024-12-16 00:19:18.524486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70d28386b04c'
down_revision: Union[str, None] = 'c28d1aae0099'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('storage', sa.Column('product_id', sa.Integer(), nullable=False))
    op.drop_index('ix_storage_name', table_name='storage')
    op.create_index(op.f('ix_storage_product_id'), 'storage', ['product_id'], unique=True)
    op.drop_column('storage', 'description')
    op.drop_column('storage', 'price')
    op.drop_column('storage', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('storage', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('storage', sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('storage', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_storage_product_id'), table_name='storage')
    op.create_index('ix_storage_name', 'storage', ['name'], unique=False)
    op.drop_column('storage', 'product_id')
    # ### end Alembic commands ###
