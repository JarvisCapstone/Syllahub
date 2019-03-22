from app import db, login
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_utils import Timestamp
from sqlalchemy import ForeignKeyConstraint, MetaData


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


course_clo_table = db.Table('course_clo',
    db.Column('course_name', db.Integer, primary_key=True),
    db.Column('course_version', db.Integer, primary_key=True),
    db.Column('clo_id', db.Integer, db.ForeignKey('clo.id'), primary_key=True),

    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version'])

)



class User(UserMixin, db.Model, Timestamp):
    id =            db.Column(db.Integer, primary_key=True)
    username =      db.Column(db.String(64), index=True, unique=True)
    email =         db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission =    db.Column(db.Enum('admin', 'instructor'), default='instructor')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    



class Syllabus(db.Model, Timestamp):
    section =            db.Column(db.Integer, primary_key=True)
    semester =           db.Column(db.Enum('spring', 'summer', 'fall'), primary_key=True)
    year =               db.Column(db.Integer, primary_key=True)
    version =            db.Column(db.Integer, primary_key=True)
    course_number =      db.Column(db.Integer, primary_key=True) #, foreign_key=True
    course_version =     db.Column(db.Integer, primary_key=True) #, foreign_key=True
    state =              db.Column(db.Enum('approved', 'draft'), default='draft')
    pdf =                db.Column(db.LargeBinary, nullable=True)
    calender =           db.Column(db.LargeBinary, nullable=True)
    schedule =           db.Column(db.LargeBinary, nullable=True)
    required_materials = db.Column(db.String(256), nullable=True)
    optional_materials = db.Column(db.String(256), nullable=True)
    withdrawl_date =     db.Column(db.String(100), nullable=True)
    grading_policy =     db.Column(db.String(500), nullable=True)
    attendance_policy =  db.Column(db.String(500), nullable=True)
    cheating_policy =    db.Column(db.String(500), nullable=True)
    extra_policies =     db.Column(db.String(500), nullable=True)
    meeting_time =       db.Column(db.String(100), nullable=True)
    meeting_dates =      db.Column(db.String(100), nullable=True)
    University_cheating_policy = db.Column(db.String(500))
    Students_with_disabilities = db.Column(db.String(500))

    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['Course.number', 'Course.version'])

    def getPDF(): 
        #ToDo
        return "pdf"
    
class Course(db.Model, Timestamp):
    number =        db.Column(db.Integer, primary_key=True)
    version =       db.Column(db.Integer, primary_key=True)
    name =          db.Column(db.String(50))
    description =   db.Column(db.String(256))
    prerequisites = db.Column(db.String(256))
    building =      db.Column(db.String(70))
    room =          db.Column(db.String(50))
    is_core =       db.Column(db.Boolean)
    is_wi =         db.Column(db.Boolean)
    is_elr =        db.Column(db.Boolean)
    is_diversity =  db.Column(db.Boolean)
    
    syllabi =       db.relationship('Syllabus', backref='course', lazy=True)
    
    clos =          db.relationship('clo', 
                                     secondary=course_clo_table,
                                     back_populates='courses')

class CLO(db.Model, Timestamp):
    id =       db.Column(db.Integer, primary_key=True)
    general =  db.Column(db.String(256))
    specific = db.Column(db.String(256))

    courses =  db.relationship('clo', 
                               secondary=course_clo_table,
                               back_populates='clos')

class Instructor(db.Model, Timestamp):
    id =                    db.Column(db.Integer, primary_key=True)
    name =                  db.Column(db.String(64), index=True)
    phone =                 db.Column(db.Integer)
    email =                 db.Column(db.String(120), index=True, unique=True)
    perfered_office_hours = db.Column(db.String(256))
    
