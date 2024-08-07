"""Adding Project entity

Revision ID: d919f20fe946
Revises: None
Create Date: 2019-03-10 14:29:12.101451

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from arctic_office_projects_api.utils import generate_countries_enum

# revision identifiers, used by Alembic.
revision = 'd919f20fe946'
down_revision = None
branch_labels = None
depends_on = None

ProjectCountry = generate_countries_enum(name='ProjectCountries')
project_countries = [name for name, member in ProjectCountry.__members__.items()]


def upgrade():
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('acronym', sa.Text(), nullable=True),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('publications', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('access_duration', postgresql.DATERANGE, nullable=False),
        sa.Column('project_duration', postgresql.DATERANGE, nullable=False),
        sa.Column('country', sa.Enum(*project_countries, name='project_country'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_neutral_id'), 'projects', ['neutral_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_projects_neutral_id'), table_name='projects')
    op.drop_table('projects')
    sa.Enum(name='project_country').drop(op.get_bind(), checkfirst=False)
