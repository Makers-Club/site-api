"""empty message

Revision ID: 1f961d0cdcc2
Revises: 7ebf40c5c0e8
Create Date: 2021-09-14 12:11:29.445086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f961d0cdcc2'
down_revision = '7ebf40c5c0e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('message', sa.String(length=512), nullable=False),
    sa.Column('user_handle', sa.String(length=128), nullable=True),
    sa.Column('user_link', sa.String(length=128), nullable=True),
    sa.Column('sprint_number', sa.String(length=128), nullable=True),
    sa.Column('sprint_link', sa.String(length=128), nullable=True),
    sa.Column('project_name', sa.String(length=128), nullable=True),
    sa.Column('project_link', sa.String(length=128), nullable=True),
    sa.Column('type', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
