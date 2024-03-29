""" create new syllabus table

Revision ID: 239ae4d7d3f4
Revises: 36718059f24d
Create Date: 2019-03-22 01:00:58.578183

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '239ae4d7d3f4'
down_revision = '36718059f24d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('syllabus',
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('section', sa.Integer(), nullable=False),
        sa.Column('semester', sa.Enum('spring', 'summer', 'fall'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('course_number', sa.Integer(), nullable=False),
        sa.Column('course_version', sa.Integer(), nullable=False),
        sa.Column('state', sa.Enum('approved', 'draft'), nullable=True),
        sa.Column('pdf', sa.LargeBinary(), nullable=True),
        sa.Column('calender', sa.LargeBinary(), nullable=True),
        sa.Column('schedule', sa.LargeBinary(), nullable=True),
        sa.Column('required_materials', sa.String(length=256), nullable=True),
        sa.Column('optional_materials', sa.String(length=256), nullable=True),
        sa.Column('withdrawl_date', sa.String(length=100), nullable=True),
        sa.Column('grading_policy', sa.String(length=500), nullable=True),
        sa.Column('attendance_policy', sa.String(length=500), nullable=True),
        sa.Column('cheating_policy', sa.String(length=500), nullable=True),
        sa.Column('extra_policies', sa.String(length=500), nullable=True),
        sa.Column('meeting_time', sa.String(length=100), nullable=True),
        sa.Column('meeting_dates', sa.String(length=100), nullable=True),
        sa.Column('University_cheating_policy', sa.String(length=500), 
                  nullable=True),
        sa.Column('Students_with_disabilities', sa.String(length=500), 
                  nullable=True),
        sa.PrimaryKeyConstraint('section', 'semester', 'year', 'version', 
                                'course_number', 'course_version'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table('syllabus')
    # ### end Alembic commands ###
