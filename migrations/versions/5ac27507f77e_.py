"""empty message

Revision ID: 5ac27507f77e
Revises: 0da61d9681b1
Create Date: 2022-07-04 08:48:21.031867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac27507f77e'
down_revision = '0da61d9681b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('lead_project', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'lead_project')
    # ### end Alembic commands ###