"""empty message

Revision ID: 312c6835d045
Revises: 12f7718d5a6e
Create Date: 2020-07-11 23:05:41.534104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '312c6835d045'
down_revision = '12f7718d5a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###