""" Change instructor phone

Revision ID: 483040bd8cda
Revises: 3539d79a1c0b
Create Date: 2019-05-01 00:42:10.910359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483040bd8cda'
down_revision = '3539d79a1c0b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE instructor change phone phone varchar(25)')
    # ### end Alembic commands ###


def downgrade():
    op.execute('ALTER TABLE instructor change phone phone int(11)')

    # ### end Alembic commands ###
