from app import create_app, db
from app.models import *
import factory

app = create_app()

#print("db in flaskapp.py=", db)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 

        'Instructor': Instructor,
        'Clo': Clo,
        'Course': Course,
        'Syllabus': Syllabus,
        'SyllabusInstructorAssociation': SyllabusInstructorAssociation,
        'User': User, 

        'factory': factory, 
    }
