"""edit users permissions

Revision ID: 1b28549721c7
Revises: 5227cc04a220
Create Date: 2019-03-31 23:03:08.140190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b28549721c7'
down_revision = '5227cc04a220'
branch_labels = None
depends_on = None


options = mysql.ENUM('admin', 'instructor')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.execute("ALTER TABLE user ALTER COLUMN permission SET DEFAULT 'instructor'")
    op.alter_column(
        'user', 
        'permission',
        server_default=sa.text("'instructor'"),
        existing_type=options,
        existing_server_default=None,
        existing_nullable=False, 
        existing_comment=None)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.execute("ALTER TABLE user ALTER COLUMN permission DROP DEFAULT")
    op.alter_column(
        'user', 
        'permission',
        server_default=None,
        existing_type=options,
        existing_server_default=sa.text("instructor"),
        existing_nullable=True, 
        existing_comment=None)
