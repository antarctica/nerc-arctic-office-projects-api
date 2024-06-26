"""empty message

Revision ID: 03eddf0b8e79
Revises: 5ac27507f77e
Create Date: 2022-12-15 15:25:06.893182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03eddf0b8e79'
down_revision = '5ac27507f77e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organisations', sa.Column('ror_identifier', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organisations', 'ror_identifier')
    # ### end Alembic commands ###
