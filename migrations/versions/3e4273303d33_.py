"""empty message

Revision ID: 3e4273303d33
Revises: 
Create Date: 2021-07-08 12:41:05.676042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e4273303d33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_templates',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('link', sa.String(length=128), nullable=False),
    sa.Column('author', sa.String(length=128), nullable=False),
    sa.Column('tech_dependencies', sa.String(length=128), nullable=False),
    sa.Column('role_types', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('goals', sa.String(length=128), nullable=False),
    sa.Column('quiz', sa.String(length=128), nullable=False),
    sa.Column('preview_images', sa.String(length=128), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('project_template_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('repository_link', sa.String(length=128), nullable=False),
    sa.Column('progress', sa.String(length=128), nullable=True),
    sa.Column('quiz_status', sa.String(length=128), nullable=True),
    sa.Column('roles', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['project_template_id'], ['project_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sprint_templates',
    sa.Column('project_template_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('tech_dependencies', sa.String(length=128), nullable=False),
    sa.Column('role_types', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('goals', sa.String(length=128), nullable=False),
    sa.Column('quiz', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['project_template_id'], ['project_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sprints',
    sa.Column('sprint_template_id', sa.String(length=128), nullable=True),
    sa.Column('project_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('progress', sa.String(length=128), nullable=True),
    sa.Column('quiz_status', sa.String(length=128), nullable=True),
    sa.Column('roles', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['sprint_template_id'], ['sprint_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_templates',
    sa.Column('sprint_template_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('tech_dependencies', sa.String(length=128), nullable=False),
    sa.Column('role_types', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('goals', sa.String(length=128), nullable=False),
    sa.Column('tests', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['sprint_template_id'], ['sprint_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('learn_resources',
    sa.Column('project_template_id', sa.String(length=128), nullable=True),
    sa.Column('sprint_template_id', sa.String(length=128), nullable=True),
    sa.Column('task_template_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('articles', sa.String(length=128), nullable=True),
    sa.Column('videos', sa.String(length=128), nullable=True),
    sa.Column('external_links', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['project_template_id'], ['project_templates.id'], ),
    sa.ForeignKeyConstraint(['sprint_template_id'], ['sprint_templates.id'], ),
    sa.ForeignKeyConstraint(['task_template_id'], ['task_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('task_template_id', sa.String(length=128), nullable=True),
    sa.Column('sprint_id', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('status', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['sprint_id'], ['sprints.id'], ),
    sa.ForeignKeyConstraint(['task_template_id'], ['task_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('learn_resources')
    op.drop_table('task_templates')
    op.drop_table('sprints')
    op.drop_table('sprint_templates')
    op.drop_table('projects')
    op.drop_table('project_templates')
    # ### end Alembic commands ###
