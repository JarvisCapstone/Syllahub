"""update syllabus course fks

Revision ID: 8a7f46ebafc8
Revises: aa3d80b91b1d
Create Date: 2019-04-12 16:22:21.000323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a7f46ebafc8'
down_revision = 'aa3d80b91b1d'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        constraint_name='fk_course_syllabus', 
        table_name='syllabus', 
        type_='foreignkey')

    op.create_foreign_key(
        constraint_name='fk_course_syllabus',
        source_table='syllabus', 
        referent_table='course', 
        local_cols=['course_number', 'course_version'], 
        remote_cols=['number', 'version'], 
        onupdate='CASCADE', 
        ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    op.drop_constraint(
        constraint_name='fk_course_syllabus', 
        table_name='syllabus', 
        type_='foreignkey')
    
    op.create_foreign_key(
        constraint_name='fk_course_syllabus',
        source_table='syllabus', 
        referent_table='course', 
        local_cols=['course_number', 'course_version'], 
        remote_cols=['number', 'version'])
    # ### end Alembic commands ###
