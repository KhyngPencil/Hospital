"""empty message

Revision ID: 2d4f38d82f25
Revises: 1f8b001819f8
Create Date: 2023-10-06 10:51:00.671148

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2d4f38d82f25'
down_revision = '1f8b001819f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pregnancy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=60), nullable=False))
        batch_op.drop_column('user_fullname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pregnancy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_fullname', mysql.VARCHAR(length=150), nullable=False))
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
