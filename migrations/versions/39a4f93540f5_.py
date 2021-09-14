"""empty message

Revision ID: 39a4f93540f5
Revises: 
Create Date: 2021-09-14 12:49:17.438895

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '39a4f93540f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'project_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('project_name', mysql.VARCHAR(length=128), nullable=True))
    # ### end Alembic commands ###