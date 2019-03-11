"""Adding projects entity

Revision ID: d919f20fe946
Revises: None
Create Date: 2019-03-10 14:29:12.101451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd919f20fe946'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_neutral_id'), 'projects', ['neutral_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_projects_neutral_id'), table_name='projects')
    op.drop_table('projects')
