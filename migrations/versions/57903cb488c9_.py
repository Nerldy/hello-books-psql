"""empty message

Revision ID: 57903cb488c9
Revises: 050dc63ebfcb
Create Date: 2018-05-08 10:22:14.005953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57903cb488c9'
down_revision = '050dc63ebfcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed_books', sa.Column('is_returned', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('borrowed_books', 'is_returned')
    # ### end Alembic commands ###
