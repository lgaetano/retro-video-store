"""empty message

Revision ID: 5b652fd337dc
Revises: 805d8ec74a61
Create Date: 2021-11-09 18:44:40.530359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b652fd337dc'
down_revision = '805d8ec74a61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('videos_checked_out_count', sa.Integer(), nullable=True))
    op.add_column('rental', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('video', sa.Column('available_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'available_inventory')
    op.drop_column('rental', 'due_date')
    op.drop_column('customer', 'videos_checked_out_count')
    # ### end Alembic commands ###
