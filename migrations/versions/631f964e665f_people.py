"""Adding people entity

Revision ID: 631f964e665f
Revises: d919f20fe946
Create Date: 2019-03-10 19:33:37.135571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631f964e665f'
down_revision = 'd919f20fe946'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=False),
        sa.Column('last_name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_people_neutral_id'), 'people', ['neutral_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_people_neutral_id'), table_name='people')
    op.drop_table('people')
