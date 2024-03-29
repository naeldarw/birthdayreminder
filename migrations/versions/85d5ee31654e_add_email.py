"""add email

Revision ID: 85d5ee31654e
Revises: c77a064b6e76
Create Date: 2022-09-04 10:33:28.457959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d5ee31654e'
down_revision = 'c77a064b6e76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('persons', sa.Column('email', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('persons', 'email')
    # ### end Alembic commands ###
