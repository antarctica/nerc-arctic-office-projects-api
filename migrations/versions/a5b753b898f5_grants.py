"""Adding Grant and Allocation entities

Revision ID: a5b753b898f5
Revises: e9e4026e918b
Create Date: 2019-03-25 09:04:56.602408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5b753b898f5'
down_revision = '631f964e665f'
branch_labels = None
depends_on = None


def upgrade():
    # Grant
    #
    op.create_table('grants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('reference', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('publications', postgresql.ARRAY(sa.Text(), dimensions=1, zero_indexes=True), nullable=True),
        sa.Column('duration', postgresql.DATERANGE(), nullable=False),
        sa.Column('status', sa.Enum(
            'Accepted', 'Active', 'Approved', 'Authorised', 'Closed', name='grant_status'),
            nullable=True
        ),
        sa.Column('total_funds', sa.Numeric(24, 2), nullable=False),
        sa.Column('total_funds_currency', postgresql.ENUM(
            'GBP', 'EUR', 'USD', name='grant_currency'),
            nullable=True
        ),
        sa.Column('indirect_funds', sa.Numeric(24, 2), nullable=True),
        sa.Column('indirect_funds_currency', postgresql.ENUM(
            'GBP', 'EUR', 'USD', name='grant_currency', create_type=False),
            nullable=True
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference')
    )
    op.create_index(op.f('ix_grants_neutral_id'), 'grants', ['neutral_id'], unique=True)

    # Allocation
    #
    op.create_table('allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('grant_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(('grant_id',), ['grants.id'], ),
        sa.ForeignKeyConstraint(('project_id',), ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_allocations_neutral_id'), 'allocations', ['neutral_id'], unique=True)


def downgrade():
    # Allocation
    #
    op.drop_index(op.f('ix_allocations_neutral_id'), table_name='allocations')
    op.drop_table('allocations')

    # Grant
    #
    op.drop_index(op.f('ix_grants_neutral_id'), table_name='grants')
    op.drop_table('grants')
    sa.Enum(name='grant_status').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='grant_currency').drop(op.get_bind(), checkfirst=False)
