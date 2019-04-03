"""Adding Organisation entity

Revision ID: 0576cef39dd8
Revises: a5b753b898f5
Create Date: 2019-03-27 07:18:10.785423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0576cef39dd8'
down_revision = 'a5b753b898f5'
branch_labels = None
depends_on = None


def upgrade():
    # Organisation
    #
    op.create_table('organisations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('grid_identifier', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('acronym', sa.Text(), nullable=True),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('logo_url', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organisations_neutral_id'), 'organisations', ['neutral_id'], unique=True)

    # Grants
    #
    op.add_column('grants', sa.Column('organisation_id', sa.Integer(), nullable=False))
    op.create_foreign_key('grants_organisation_id_fkey', 'grants', 'organisations', ['organisation_id'], ['id'])

    # People
    #
    op.add_column('people', sa.Column('organisation_id', sa.Integer(), nullable=False))
    op.create_foreign_key('people_organisation_id_fkey', 'people', 'organisations', ['organisation_id'], ['id'])


def downgrade():
    # People
    #
    op.drop_constraint('people_organisation_id_fkey', 'people', type_='foreignkey')
    op.drop_column('people', 'organisation_id')

    # Grants
    #
    op.drop_constraint('grants_organisation_id_fkey', 'grants', type_='foreignkey')
    op.drop_column('grants', 'organisation_id')

    # Organisation
    #
    op.drop_index(op.f('ix_organisations_neutral_id'), table_name='organisations')
    op.drop_table('organisations')
