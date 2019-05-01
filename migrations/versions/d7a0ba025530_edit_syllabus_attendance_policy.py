"""edit syllabus attendance policy

Revision ID: d7a0ba025530
Revises: 483040bd8cda
Create Date: 2019-05-01 01:16:25.737830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a0ba025530'
down_revision = '483040bd8cda'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE syllabus change attendance_policy attendance_policy varchar(1000)')
    op.execute('ALTER TABLE syllabus change extra_policies extra_policies varchar(1000)')
    op.execute('ALTER TABLE syllabus change Students_with_disabilities Students_with_disabilities varchar(1000)')
    # ### end Alembic commands ###


def downgrade():
    op.execute('ALTER TABLE syllabus change attendance_policy attendance_policy varchar(500)')
    op.execute('ALTER TABLE syllabus change extra_policies extra_policies varchar(500)')
    op.execute('ALTER TABLE syllabus change Students_with_disabilities Students_with_disabilities varchar(500)')
    # ### end Alembic commands ###
