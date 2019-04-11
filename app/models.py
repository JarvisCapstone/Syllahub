from app import db, login
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_utils import Timestamp
from sqlalchemy import and_, Boolean, Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, MetaData, String, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy


@login.user_loader
def load_user(id):
    ''' Used by Flask-Login to login user

    Args: 
        primary key of User
    
    Returns: 
        User with primary key = to Args
    '''
    return User.query.get(int(id))


# Association Tables/Objects --------------------------------------------------
class SyllabusInstructorAssociation(db.Model):
    ''' Association object relating Instructor and Syllabus

    Since instructors have a jobs such as teacher, grader, ect that may
    appear on many syllabi, SqlAlchemy requires an association object

    TODO: consider making this not a model but share Base
    '''

    __tablename__ = 'syllabus_instructor'
    
    # Primary Keys for Syllabus    
    syllabus_course_number = Column(Integer, primary_key=True)
    syllabus_course_version = Column(Integer, primary_key=True)
    syllabus_section = Column(Integer, primary_key=True)
    syllabus_semester = Column(Enum('spring', 'summer', 'fall'), 
                               primary_key=True)
    syllabus_version = Column(Integer, primary_key=True)
    syllabus_year = Column(Integer, primary_key=True)

    # Primary and Foreign Key for Instructor    
    instructor_id = Column(Integer, ForeignKey('instructor.id'), 
                           primary_key=True)

    # Foreign Keys for Syllabus    
    ForeignKeyConstraint(
        [
            'syllabus_section',
            'syllabus_semester',
            'syllabus_year',
            'syllabus_version',
            'syllabus_course_number',
            'syllabus_course_version',
        ],

        [
            'syllabus.section',
            'syllabus.semester',
            'syllabus.year',
            'syllabus.version',
            'syllabus.course_number',
            'syllabus.course_version',
        ])

    # Relationships
    instructor = relationship(
        "Instructor", # mapped class representing target of relationship
        primaryjoin="SyllabusInstructorAssociation.instructor_id "
                        "== Instructor.id",

        remote_side="Instructor.id",
        foreign_keys="SyllabusInstructorAssociation.instructor_id",

        backref=backref("instructorSyllabusAssociationList"))
        #back_populates="syllabi")

    syllabus =  relationship(
        # use strings in relationships to avoid reference errors
        
        "Syllabus", # mapped class representing target of relationship
        
        primaryjoin=
            "and_(SyllabusInstructorAssociation.syllabus_section"
                      " == Syllabus.section, "
                 "SyllabusInstructorAssociation.syllabus_semester"
                      " == Syllabus.semester, "
                 "SyllabusInstructorAssociation.syllabus_year"
                      " == Syllabus.year, "
                 "SyllabusInstructorAssociation.syllabus_version"
                      " == Syllabus.version, "
                 "SyllabusInstructorAssociation.syllabus_course_number"
                      " == Syllabus.course_number, "
                 "SyllabusInstructorAssociation.syllabus_course_version"
                      " == Syllabus.course_version)",

        remote_side=
            "["
                "Syllabus.section, "
                "Syllabus.semester, "
                "Syllabus.year, "
                "Syllabus.version, "
                "Syllabus.course_number, "
                "Syllabus.course_version,"
            "]",

        foreign_keys= 
            "["
                "SyllabusInstructorAssociation.syllabus_section,"
                "SyllabusInstructorAssociation.syllabus_semester,"
                "SyllabusInstructorAssociation.syllabus_year,"
                "SyllabusInstructorAssociation.syllabus_version,"
                "SyllabusInstructorAssociation.syllabus_course_number,"
                "SyllabusInstructorAssociation.syllabus_course_version,"
            "]",

        backref=backref("syllabusInstructorAssociationList"))
        #back_populates="syllabusInstructorAssociationList")

    # Non Key Columns
    job_on_syllabus = Column(String(120))


    def __repr__(self):
        '''returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return "<SyllabusInstructorAssociation \n" \
            "\tsyllabus_course_number={} \n" \
            "\tsyllabus_course_version={} \n" \
            "\tsyllabus_section={} \n" \
            "\tsyllabus_semester={} \n" \
            "\tsyllabus_version={} \n" \
            "\tsyllabus_year={} \n" \
            "\tinstructor_id={} \n" \
            "\tinstructor={} \n" \
            "\tsyllabus={} \n" \
            "\tjob_on_syllabus={} \n>" \
            .format(self.syllabus_course_number, 
                    self.syllabus_course_version, 
                    self.syllabus_section, self.syllabus_semester, 
                    self.syllabus_version, self.syllabus_year,
                    self.instructor_id, 
                    self.instructor,
                    self.syllabus,
                    self.job_on_syllabus)


# SqlAlchemy requires a table to define the many to many relationship between 
# course and clo
course_clo_table = db.Table(
    'course_clo', # Table Name

    # Primary Keys for Course
    Column('course_number', Integer, primary_key=True),
    Column('course_version', Integer, primary_key=True),
    
    # Primary and Foreign Key for Clo
    Column('clo_id', Integer, ForeignKey('clo.id'), primary_key=True),
    
    # Foreign Keys for Course
    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version']))

# Models ----------------------------------------------------------------------
class Clo(db.Model, Timestamp):
    '''CLO model

    No Foreign Keys
    '''

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Relationships    
    courses = db.relationship('Course', secondary=course_clo_table,
                              back_populates='clos')
    
    # Non Key Columns
    general = db.Column(db.String(256))
    specific = db.Column(db.String(256))


    def __repr__(self):
        '''returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return '<CLO id={}>'.format(self.id)



class Course(db.Model, Timestamp):
    '''Course Model

    No Foreign Keys
    Relationship with Syllabus
        one to many
        Course is Parent and Syllabus is Child
    '''

    # Primary Keys
    number = Column(Integer, primary_key=True)
    version = Column(Integer, primary_key=True) # TODO: autoincrement
    
    # Relationships    
    clos = relationship('Clo', secondary=course_clo_table,
                        back_populates='courses')
    
    
    syllabi = relationship(
        "Syllabus", 
        primaryjoin="and_(Course.number == Syllabus.course_number, "
                         "Course.version == Syllabus.course_version)",
        foreign_keys="[Syllabus.course_number, Syllabus.course_version]",
        remote_side="[Syllabus.course_number, Syllabus.course_version]",
        back_populates="course")   
    

    # Non Key Columns
    building = Column(String(70))
    description = Column(String(256))
    is_core = Column(Boolean)
    is_diversity = Column(Boolean)
    is_elr = Column(Boolean)
    is_wi = Column(Boolean)
    name = Column(String(50))
    prerequisites = Column(String(256))
    room = Column(String(50))


    def __repr__(self):
        '''Returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return '<Course number={} version={}>'.format(self.number, self.version)



class Instructor(db.Model, Timestamp):
    '''Instructor Model

    No Foreign Keys
    Relationship with Syllabus
        many to many
        Relatiohship to SyllabusInstructorAssociation
            one to many
            Parent is SyllabusInstructorAssociation
            Child is Instructor
    
    Relationship with User
        one to zero/one
    '''

    # Primary Key
    id = Column(Integer, primary_key=True)
    
    # Association Proxies
    # Associates Instructor.instructorSyllabusAssociationList relationship with the
    # SyllabusInstructorAssociation.syllabus relationship
    syllabusList = association_proxy('instructorSyllabusAssociationList', 'syllabus')

    # Relationships
    user = relationship("User", uselist=False, back_populates="instructor")


    # Non Key Columns
    email = Column(String(120), index=True, unique=True)
    name = Column(String(64), index=True)
    phone = Column(Integer)
    perfered_office_hours = Column(String(256))
    

    def __repr__(self):
        '''returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return '<Instructor id={} name={}>'.format(self.id, self.name)



class Syllabus(db.Model, Timestamp):
    '''Syllabus Model

    Relationship with Course
        many to one
        course is parent and syllabus is child
    '''

    # Primary Keys
    course_number = Column(Integer, primary_key=True)
    course_version = Column(Integer, primary_key=True)
    section = Column(Integer, primary_key=True)
    semester = Column(Enum('spring', 'summer', 'fall'), primary_key=True)
    version = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    
    # Foreign Keys
    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version'])

    # Association Proxies
    instructorList = association_proxy('syllabusInstructorAssociationList', 'instructor')


    # Relationships  
    course = relationship(
        "Course", 
        primaryjoin="and_(Syllabus.course_number == Course.number, "
                         "Syllabus.course_version == Course.version)",
        #uselist=False
        remote_side="[Course.number, Course.version]",
        foreign_keys="[Syllabus.course_number, Syllabus.course_version]",
        
        back_populates="syllabi")   
    

    # Non Key Columns
    attendance_policy = Column(String(500), nullable=True)
    calender = Column(LargeBinary, nullable=True)
    cheating_policy = Column(String(500), nullable=True)
    extra_policies = Column(String(500), nullable=True)
    grading_policy = Column(String(500), nullable=True)
    meeting_dates = Column(String(100), nullable=True)
    meeting_time = Column(String(100), nullable=True)
    optional_materials = Column(String(256), nullable=True)
    pdf = Column(LargeBinary, nullable=True)
    required_materials = Column(String(256), nullable=True)
    schedule = Column(LargeBinary, nullable=True)
    state = Column(Enum('approved', 'draft'), default='draft')
    Students_with_disabilities = Column(String(500))
    University_cheating_policy = Column(String(500))
    withdrawl_date = Column(String(100), nullable=True)

    def addInstructor(self, instructor, job):
        '''Add an association between syllabus and instructor
        TODO: Test if this works flawlessly. Has not been tested
        '''
        new_job = SyllabusInstructorAssociation(job_on_syllabus=job)
        new_job.instructor = instructor;
        new_job.syllabus = self;
        db.session.add(new_job)
        db.session.commit()

    def __repr__(self):
        '''returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return "<Syllabus \n" \
            "\tcourse_number={} \n" \
            "\tcourse_version={} \n" \
            "\tsection={} \n" \
            "\tsemester={} \n" \
            "\tversion={} \n" \
            "\tyear={}\n>" \
            .format(self.course_number, self.course_version, 
                    self.section, self.semester, 
                    self.version, self.year)



class User(UserMixin, db.Model, Timestamp):
    '''User Model
    Relationship with Instructor
        one to one
    '''
    # TODO: make email primary key
    # TODO: remove id and username from db 

    # Primary Keys
    email = Column(String(120), primary_key=True)

    # Foreign Keys
    instructor_id = Column(Integer, ForeignKey('instructor.id'), nullable=True)
    
    # Relationships    
    instructor = relationship("Instructor", back_populates="user")

    # Non Key Columns
    password_hash = Column(String(128), nullable=False)
    permission = Column(Enum('admin', 'instructor'), nullable=False, 
                        server_default=text("instructor"))
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def isAdmin(self):
        return self.permission == 'admin'

    def __repr__(self):
        '''returns a printable representation of the object. 

        Determines the result of when class is called in Print()
        '''
        return '<User email={}>'.format(self.email)    


