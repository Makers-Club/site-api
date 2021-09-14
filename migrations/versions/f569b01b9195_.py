"""empty message

Revision ID: f569b01b9195
Revises: 0500723ab8c4
Create Date: 2021-09-14 09:34:51.990556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f569b01b9195'
down_revision = '0500723ab8c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sprints', sa.Column('number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sprints', 'number')
    # ### end Alembic commands ###