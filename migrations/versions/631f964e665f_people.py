"""Adding Person and Participant entities

Revision ID: 631f964e665f
Revises: d919f20fe946
Create Date: 2019-03-10 19:33:37.135571

"""
from alembic import op
import sqlalchemy as sa

from arctic_office_projects_api.models import ParticipantRole

# revision identifiers, used by Alembic.
revision = '631f964e665f'
down_revision = 'd919f20fe946'
branch_labels = None
depends_on = None

participant_roles = [name for name, member in ParticipantRole.__members__.items()]


def upgrade():
    # Person
    #
    op.create_table('people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('orcid_id', sa.String(length=64), nullable=True),
        sa.Column('logo_url', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('orcid_id')
    )
    op.create_index(op.f('ix_people_neutral_id'), 'people', ['neutral_id'], unique=True)

    # Participant
    #
    op.create_table('participants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum(*participant_roles, name='participant_role'), nullable=True),
        sa.ForeignKeyConstraint(('person_id',), ['people.id'], ),
        sa.ForeignKeyConstraint(('project_id',), ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_participants_neutral_id'), 'participants', ['neutral_id'], unique=True)


def downgrade():
    # Participant
    #
    op.drop_index(op.f('ix_participants_neutral_id'), table_name='participants')
    op.drop_table('participants')
    sa.Enum(name='participant_role').drop(op.get_bind(), checkfirst=False)

    # Person
    #
    op.drop_index(op.f('ix_people_neutral_id'), table_name='people')
    op.drop_table('people')
