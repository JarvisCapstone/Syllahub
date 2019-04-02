from app import db, login
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_utils import Timestamp
from sqlalchemy import ForeignKeyConstraint, MetaData, and_


@login.user_loader
def load_user(id):
    print('id=', id)
    return User.query.get(int(id))



class SyllabusInstructorAssociation(db.Model):
    __tablename__ = 'syllabus_instructor'
    
    instructor_id =  db.Column(db.Integer, db.ForeignKey('Instructor.id'), primary_key=True)
    syllabus_section =            db.Column(db.Integer, primary_key=True)
    syllabus_semester =           db.Column(db.Enum('spring', 'summer', 'fall'), primary_key=True)
    syllabus_year =               db.Column(db.Integer, primary_key=True)
    syllabus_version =            db.Column(db.Integer, primary_key=True)
    syllabus_course_number =      db.Column(db.Integer, primary_key=True)
    syllabus_course_version =     db.Column(db.Integer, primary_key=True)

    job_on_syllabus =             db.Column(db.String(120))

    ForeignKeyConstraint(
        ['syllabus_section',
         'syllabus_semester',
         'syllabus_year',
         'syllabus_version',
         'syllabus_course_number',
         'syllabus_course_version'],

        ['syllabus.section',
         'syllabus.semester',
         'syllabus.year',
         'syllabus.version',
         'syllabus.course_number',
         'syllabus.course_version']
        )


    instructor = db.relationship(
        "Instructor",               # argument : mapped class representing target of relationship
        primaryjoin="SyllabusInstructorAssociation.instructor_id == Instructor.id",
        foreign_keys="Instructor.id",
        backref="syllabi"    # takes a string. complementary property should back_populate to this relationship
        )


    syllabus =  db.relationship(    # use strings in relationships to avoid reference errors
        "Syllabus",                    # argument : mapped class representing target of relationship
        primaryjoin="and_(SyllabusInstructorAssociation.syllabus_section == Syllabus.section, "
                         "SyllabusInstructorAssociation.syllabus_semester == Syllabus.semester, "
                         "SyllabusInstructorAssociation.syllabus_year == Syllabus.year, "
                         "SyllabusInstructorAssociation.syllabus_version == Syllabus.version, "
                         "SyllabusInstructorAssociation.syllabus_course_number == Syllabus.course_number, "
                         "SyllabusInstructorAssociation.syllabus_course_version == Syllabus.course_version)"
        ,
        foreign_keys="[Syllabus.section, Syllabus.semester, Syllabus.year, Syllabus.version, Syllabus.course_number, Syllabus.course_version]",
        backref="instructors"    # takes a string. complementary property should back_populate to this relationship
        )


course_clo_table = db.Table('course_clo',
    # used to define the many to many relationship between course and clo
    db.Column('course_number',  db.Integer, primary_key=True),
    db.Column('course_version', db.Integer, primary_key=True),
    
    db.Column('clo_id', db.Integer, db.ForeignKey('clo.id'), primary_key=True),

    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version'])
)


class User(UserMixin, db.Model, Timestamp):
    id =            db.Column(db.Integer, primary_key=True)
    username =      db.Column(db.String(64),  nullable=False, index=True, unique=True)
    email =         db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    permission =    db.Column(db.Enum('admin', 'instructor'), 
                              nullable=False, 
                              server_default=db.text("instructor")) #default='instructor')
    instructor_id = db.Column(db.Integer, 
                              db.ForeignKey('instructor.id'), 
                              nullable=True)
    instructor = db.relationship("Instructor")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Syllabus(db.Model, Timestamp):
    section =            db.Column(db.Integer, primary_key=True)
    semester =           db.Column(db.Enum('spring', 'summer', 'fall'), 
                                    primary_key=True)
    year =               db.Column(db.Integer, primary_key=True)
    version =            db.Column(db.Integer, primary_key=True)
    course_number =      db.Column(db.Integer, primary_key=True)
    course_version =     db.Column(db.Integer, primary_key=True)
    state =              db.Column(db.Enum('approved', 'draft'), 
                                   default='draft')
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
                         ['course.number', 'course.version'])

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
    
    #syllabi =       db.relationship('Syllabus', backref='course', lazy=True)
    
    clos =          db.relationship('Clo', 
                                     secondary=course_clo_table,
                                     back_populates='courses')

class Clo(db.Model, Timestamp):
    id =       db.Column(db.Integer, primary_key=True)
    general =  db.Column(db.String(256))
    specific = db.Column(db.String(256))

    courses =  db.relationship('Course', 
                               secondary=course_clo_table,
                               back_populates='clos')

class Instructor(db.Model, Timestamp):
    id =                    db.Column(db.Integer, primary_key=True)
    name =                  db.Column(db.String(64), index=True)
    phone =                 db.Column(db.Integer)
    email =                 db.Column(db.String(120), index=True, unique=True)
    perfered_office_hours = db.Column(db.String(256))
    
    user    = db.relationship("User", uselist=False, 
                              back_populates="instructor")

    def __repr__(self):
        return '<Instructor id={} name={}>'.format(self.id, self.name)







'''
class SyllabusInstructorAssociation(db.Model):
    # Since instructors have a jobs such as teacher, grader, ect that may
    # appear on many syllabi, SqlAlchemy requires an association object
    __tablename__ = 'syllabus_instructor'

    #syllabus_section =            db.Column(db.Integer, primary_key=True)
    #syllabus_semester =           db.Column(db.Enum('spring', 
    #                                                'summer', 
    #                                                'fall'), 
    #                                        primary_key=True)
    syllabus_year =               db.Column(db.Integer, primary_key=True)
    ###syllabus_year =               db.Column(db.Integer, db.ForeignKey('syllabus.year'), primary_key=True)
    #syllabus_version =            db.Column(db.Integer, primary_key=True)
    #syllabus_course_number =      db.Column(db.Integer, primary_key=True) 
    #syllabus_course_version =     db.Column(db.Integer, primary_key=True) 

    instructor_id =               db.Column(db.Integer, 
                                            db.ForeignKey('instructor.id'), 
                                            primary_key=True)

    job_on_syllabus =             db.Column(db.String(120))

    ForeignKeyConstraint([#'syllabus_section',       'syllabus_semester', 
                          'syllabus_year',        #  'syllabus_version', 
                          #'syllabus_course_number', 'syllabus_course_version'
                          ], 

                         [#'syllabus.section',       'syllabus.semester', 
                          'syllabus.year',        #  'syllabus.version', 
                          #'syllabus.course_number', 'syllabus.course_version'
                          ])
    
    instructor = db.relationship("Instructor", back_populates="syllabi")
    syllabus   = db.relationship("Syllabus", 
        #primaryjoin= db.text('syllabus_instructor.syllabus_year == syllabus.year'),
        #primaryjoin= syllabus_year == syllabus.c.year,
        #primaryjoin= and_(syllabus_year == ),
        foreign_keys=syllabus_year, 
        #foreign_keys=[syllabus_year, syllabus_version], 
        back_populates="instructors")
    '''