"""empty message

Revision ID: fa7aa1816638
Revises: 2dbbd7cb784c
Create Date: 2018-05-10 17:09:59.155089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa7aa1816638'
down_revision = '2dbbd7cb784c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrowed_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('borrow_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book_list.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrowed_books')
    # ### end Alembic commands ###
