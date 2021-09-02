"""empty message

Revision ID: a822bc99ab5c
Revises: 
Create Date: 2021-09-01 22:04:06.761163

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a822bc99ab5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_tokens', sa.Column('client_id', sa.String(length=128), nullable=False))
    op.add_column('api_tokens', sa.Column('id', sa.String(length=128), nullable=False))
    op.drop_column('api_tokens', 'access_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_tokens', sa.Column('access_token', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('api_tokens', 'id')
    op.drop_column('api_tokens', 'client_id')
    # ### end Alembic commands ###
