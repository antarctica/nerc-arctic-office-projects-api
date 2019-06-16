"""Adding category entities

Revision ID: fe26d37d220f
Revises: 0576cef39dd8
Create Date: 2019-05-28 09:41:14.512245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
from sqlalchemy_utils import LtreeType

revision = 'fe26d37d220f'
down_revision = '0576cef39dd8'
branch_labels = None
depends_on = None


def upgrade():
    # CategoryScheme
    #
    op.create_table('category_schemes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('acronym', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.Text(), nullable=True),
        sa.Column('revision', sa.Text(), nullable=True),
        sa.Column('namespace', sa.Text(), nullable=False),
        sa.Column('root_concepts', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_schemes_neutral_id'), 'category_schemes', ['neutral_id'], unique=True)

    # CategoryTerm
    #
    op.execute("CREATE EXTENSION IF NOT EXISTS ltree")
    op.create_table('category_terms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_scheme_id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('scheme_identifier', sa.Text(), nullable=False),
        sa.Column('scheme_notation', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('aliases', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('definitions', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('examples', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('notes', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('scope_notes', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('path', LtreeType(), nullable=False),
        sa.ForeignKeyConstraint(('category_scheme_id',), ['category_schemes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_terms_neutral_id'), 'category_terms', ['neutral_id'], unique=True)
    op.create_index(op.f('ix_category_terms_path'), 'category_terms', ['path'], unique=False)

    # Categorisation
    #
    op.create_table('categorisations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('category_term_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(('category_term_id',), ['category_terms.id'], ),
        sa.ForeignKeyConstraint(('project_id',), ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorisations_neutral_id'), 'categorisations', ['neutral_id'], unique=True)
    op.create_unique_constraint('uq_categorisations_project_category_term', 'categorisations', [
        'project_id',
        'category_term_id'
    ])


def downgrade():
    # Categorisation
    #
    op.drop_index(op.f('ix_categorisations_neutral_id'), table_name='category_schemes')
    op.drop_constraint(op.f('uq_categorisations_project_category_term'), table_name='categorisations')
    op.drop_table('categorisations')

    # CategoryTerm
    #
    op.drop_index(op.f('ix_category_terms_path'), table_name='category_terms')
    op.drop_index(op.f('ix_category_terms_neutral_id'), table_name='category_terms')
    op.drop_table('category_terms')
    op.execute("DROP EXTENSION IF EXISTS ltree")

    # CategoryScheme
    #
    op.drop_index(op.f('ix_category_schemes_neutral_id'), table_name='category_schemes')
    op.drop_table('category_schemes')
