"""Adding People:Projects join entity

Revision ID: e9e4026e918b
Revises: 631f964e665f
Create Date: 2019-03-10 20:11:06.267244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9e4026e918b'
down_revision = '631f964e665f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('people_projects',
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('investigative_role', sa.Enum('chief_scientist', 'co_investigator', 'collaborator', 'computer_programmer', 'consultant', 'inventor', 'post_doctoral_researcher', 'principal_investigator', 'project_student', 'research_assistant', 'research_student', 'researcher', 'scholar', 'service_engineer', 'technician', name='investigativerole'), nullable=True),
        sa.ForeignKeyConstraint(['person_id'], ['people.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('project_id', 'person_id')
    )


def downgrade():
    op.drop_table('people_projects')
    sa.Enum(name='investigativerole').drop(op.get_bind(), checkfirst=False)
