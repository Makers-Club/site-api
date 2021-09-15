"""empty message

Revision ID: e33ddeddba23
Revises: 709571f28067
Create Date: 2021-09-14 22:50:12.154661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e33ddeddba23'
down_revision = '709571f28067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('user_pic', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'user_pic')
    # ### end Alembic commands ###
