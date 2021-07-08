"""empty message

Revision ID: 5a412e98d4c9
Revises: 6d31dc99a2c5
Create Date: 2021-07-08 09:26:43.716733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a412e98d4c9'
down_revision = '6d31dc99a2c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('learn_resources',
    sa.Column('project_template_id', sa.String(length=128), nullable=True),
    sa.Column('sprint_template_id', sa.String(length=128), nullable=True),
    sa.Column('task_template_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('articles', sa.String(length=128), nullable=False),
    sa.Column('videos', sa.String(length=128), nullable=False),
    sa.Column('external_links', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['project_template_id'], ['project_templates.id'], ),
    sa.ForeignKeyConstraint(['sprint_template_id'], ['sprint_templates.id'], ),
    sa.ForeignKeyConstraint(['task_template_id'], ['task_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('learn_resources')
    # ### end Alembic commands ###