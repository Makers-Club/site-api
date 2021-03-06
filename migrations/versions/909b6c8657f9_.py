"""empty message

Revision ID: 909b6c8657f9
Revises: 011b1fa661c1
Create Date: 2021-09-15 19:44:22.192357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '909b6c8657f9'
down_revision = '011b1fa661c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('repository_link', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'repository_link')
    # ### end Alembic commands ###
