"""empty message

Revision ID: 0a22009b9386
Revises: 
Create Date: 2021-06-28 15:24:31.595478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0a22009b9386'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test', mysql.VARCHAR(length=60), nullable=True))
    # ### end Alembic commands ###
