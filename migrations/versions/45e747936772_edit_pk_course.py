""" edit course primary key

Revision ID: 45e747936772
Revises: 239ae4d7d3f4
Create Date: 2019-03-22 01:49:00.225962

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '45e747936772'
down_revision = '239ae4d7d3f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    print('step 1')
    #op.execute('ALTER TABLE course DROP CONSTRAINT pk_course')
    op.drop_constraint('PRIMARY', 'course', type_='primary')
    print('step 2')

    op.drop_column('course', 'id')
    print('step 3')

    op.create_primary_key('pk_course', 'course', ['number', 'version'])
    print('done')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    print('step 1')
    op.drop_constraint('PRIMARY', 'course', type_='primary')
    print('step 2')

    op.add_column('course', sa.Column('id', sa.Integer(), nullable=False))
    print('step 3')

    op.create_primary_key('pk_course', 'course', ['id', 'version'])
    print('done')

    #op.drop_constraint('fk_course_syllabus', 'syllabus', type_='foreignkey')
    # ### end Alembic commands ###