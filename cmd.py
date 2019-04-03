from app import db
from sqlalchemy.engine import reflection
from pprint import pprint

def getInspector(): 
    meta = db.metadata
    engine = db.engine
    insp = reflection.Inspector.from_engine(engine)
    return insp
    #insp.get_table_names()
    #insp.get_columns('user')


def inspectModel(model):
    inspectUser = inspect(model)
    #pprint(list(inspectUser.columns))
    inspectUser.relationships

