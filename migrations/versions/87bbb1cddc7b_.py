"""empty message

Revision ID: 87bbb1cddc7b
Revises: 64e2273ca11d
Create Date: 2018-04-26 17:54:15.811231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87bbb1cddc7b'
down_revision = '64e2273ca11d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_modified', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_modified')
    # ### end Alembic commands ###