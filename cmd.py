from app import db
from sqlalchemy.engine import reflection
from app.models import *
from pprint import pprint
from sqlalchemy import inspect

def getInspector(): 
    meta = db.metadata
    engine = db.engine
    insp = reflection.Inspector.from_engine(engine)
    return insp
    #insp.get_table_names()
    #insp.get_columns('user')


def inspectModel():
    inspectUser = inspect(User)
    #pprint(list(inspectUser.columns))
    inspectUser.relationships

def test():
    print('tested')

def getInstructor():
    return Instructor(name='bob',
                   phone=10,
                   email='bob@email.com',
                   perfered_office_hours='mwf10-30')

def getSyllabus():
    return Syllabus()