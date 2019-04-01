from app import create_app, db
from app.models import *
app = create_app()

#print("db in flaskapp.py=", db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'Instructor': Instructor,
            'Syllabus': Syllabus,
            'SyllabusInstructorAssociation': SyllabusInstructorAssociation
            }

def view_routes():
    for name, func in app.view_functions.items():
        print(name)
        print(func)
        print()