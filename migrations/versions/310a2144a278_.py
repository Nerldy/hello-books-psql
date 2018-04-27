"""empty message

Revision ID: 310a2144a278
Revises: 87bbb1cddc7b
Create Date: 2018-04-27 14:17:53.076001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '310a2144a278'
down_revision = '87bbb1cddc7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('middle_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_authors',
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], )
    )
    op.add_column('books', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('books', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('books', sa.Column('synopsis', sa.String(length=200), nullable=False))
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=140),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=140),
               nullable=True)
    op.drop_column('books', 'synopsis')
    op.drop_column('books', 'date_modified')
    op.drop_column('books', 'date_created')
    op.drop_table('book_authors')
    op.drop_table('authors')
    # ### end Alembic commands ###
