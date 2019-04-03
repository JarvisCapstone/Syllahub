"""edit user pk

Revision ID: 48cfb9483352
Revises: 1b28549721c7
Create Date: 2019-04-03 00:40:31.873932

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm.query import Query

# revision identifiers, used by Alembic.
revision = '48cfb9483352'
down_revision = '1b28549721c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_column('user', 'id')
    op.drop_column('user', 'username')
    op.execute('ALTER TABLE user ADD PRIMARY KEY (email)')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    
    op.add_column('user', sa.Column('created', sa.DateTime(), nullable=False))
    op.add_column('user', sa.Column('permission', sa.Enum('admin', 'instructor'), nullable=False))
    op.add_column('user', sa.Column('updated', sa.DateTime(), nullable=False))

    options = mysql.ENUM('admin', 'instructor')

    op.alter_column('user', 'permission',
               server_default=sa.text("'instructor'"),
               existing_type=options,
               existing_server_default=None,
               existing_nullable=False, 
               existing_comment=None)

    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=120),
               nullable=False)
    op.alter_column('user', 'password_hash',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)

    op.add_column('user', sa.Column('instructor_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_user_instructor', 'user', 'instructor', ['instructor_id'], ['id'])
    # ### end Alembic commands ###
