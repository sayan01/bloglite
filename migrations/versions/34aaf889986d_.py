"""empty message

Revision ID: 34aaf889986d
Revises: 7a8a4bb8585c
Create Date: 2023-01-14 18:29:14.631308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34aaf889986d'
down_revision = '7a8a4bb8585c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('favcolor')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favcolor', sa.VARCHAR(length=20), nullable=True))

    # ### end Alembic commands ###