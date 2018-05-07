"""empty message

Revision ID: ddeff5123b66
Revises: 201ebf01d184
Create Date: 2018-05-07 19:14:09.529458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddeff5123b66'
down_revision = '201ebf01d184'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_list', sa.Column('is_borrowed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book_list', 'is_borrowed')
    # ### end Alembic commands ###
