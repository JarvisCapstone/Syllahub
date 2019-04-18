from app import db, login
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_utils import Timestamp
from sqlalchemy import and_, Boolean, Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, MetaData, String, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import select, func


@login.user_loader
def load_user(email):
    '''Used by Flask-Login to login user

    Args: 
        primary key of User
    
    Returns: 
        User with primary key = to Args
    '''
    return User.query.get(email)


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
    instructor_id = Column(Integer, 
                           ForeignKey('instructor.id', onupdate="CASCADE", 
                                      ondelete="CASCADE"), 
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
        ],
        onupdate="CASCADE", 
        ondelete="CASCADE")

    # Relationships
    instructor = relationship(
        "Instructor", # mapped class representing target of relationship
        primaryjoin="SyllabusInstructorAssociation.instructor_id "
                        "== Instructor.id",

        remote_side="Instructor.id",
        foreign_keys="SyllabusInstructorAssociation.instructor_id",

        backref=backref("instructorSyllabusAssociationList"))

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

    # Non Key Columns
    job_on_syllabus = Column(String(120))

    def create(syllabus, instructor, job):
        '''Add an association between syllabus and instructor
        TODO: Test if this works flawlessly. Has not been tested

        Args: 
            syllabus: Syllabus - 
            instructor: Instructor - 
            job: String - 
        '''
        new_job = SyllabusInstructorAssociation(job_on_syllabus=job)
        new_job.instructor = instructor;
        new_job.syllabus = syllabus;
        db.session.add(new_job)
        db.session.commit()

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
    Column('clo_id', Integer, 
           ForeignKey('clo.id', onupdate="CASCADE", ondelete="CASCADE"), 
           primary_key=True),
    
    # Foreign Keys for Course
    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version'],
                         onupdate="CASCADE", ondelete="CASCADE"))

# Models ---------------------------------------------------------------------
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
    # Number CS0001
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
    building = Column(String(70)) # TODO, remove (move to syllabus)
    description = Column(String(256))
    is_core = Column(Boolean)
    is_diversity = Column(Boolean)
    is_elr = Column(Boolean)
    is_wi = Column(Boolean)
    name = Column(String(50)) #EX: CS3
    prerequisites = Column(String(256))
    room = Column(String(50)) # TODO, remove (move to syllabus)


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
    syllabusList = association_proxy('instructorSyllabusAssociationList', 'syllabus')

    # Relationships
    user = relationship("User", uselist=False, back_populates="instructor")


    # Non Key Columns
    email = Column(String(120), index=True, unique=True)
    name = Column(String(64), index=True)
    phone = Column(Integer) # TODO change this to string
    perfered_office_hours = Column(String(256))
    
    def addToSyllabus(self, syllabus, job):
        '''Add an association between syllabus and instructor
        TODO: Test if this works flawlessly. Has not been tested

        Args: 
            syllabus: Syllabus - 
            job: String - 
        '''
        syllabus.addInstructor(self,job)
        SyllabusInstructorAssociation.create(syllabus, self, job)

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
    # CRN course_registration_number used as a primary key in school db
    # does not appear on syllabus

    course_number = Column(Integer, primary_key=True)
    course_version = Column(Integer, primary_key=True)
    
    section = Column(Integer, primary_key=True) # TODO change to string(3)
    semester = Column(Enum('spring', 'summer', 'fall'), primary_key=True)
    version = Column(
                  Integer, primary_key=True)#,default=generateSyllabusVersion()) # TODO set to autoincrement
                  #default=select([func.max(1,func.max('syllabus.c.version'))])) # TODO set to autoincrement


    #[func.max(1,func.max(version_table.c.old_versions))]
    year = Column(Integer, primary_key=True)
    
    # Foreign Keys
    ForeignKeyConstraint(['course_number', 'course_version'], 
                         ['course.number', 'course.version'], 
                         onupdate="CASCADE", ondelete="CASCADE")

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
    

    # Defaults
    # TODO set default policy information to variables here. 
    currentCheatingPolicy = "University policy 3-01.8 deals with the problem of academic dishonesty, cheating, and plagiarism.  None of these will be tolerated in this class.  The sanctions provided in this policy will be used to deal with any violations.  If you have any questions, please read the policy at http://www.kent.edu/policyreg/administrative-policy-regarding-student-cheating-and-plagiarism and/or ask."
    currentAttendancePolicy = "Regular attendance in class is expected of all students at all levels at the university. While classes are conducted on the premise that regular attendance is expected, the university recognizes certain activities, events, and circumstances as legitimate reasons for absence from class. This policy provides for accommodations in accordance with federal and state laws prohibiting discrimination, including, but not limited to, Section 504 of the Rehabilitation Act of 1973, 29 U.S.C.§794, and its implementing regulation, 34 C.F.R. Part 104; Title II of the Americans with Disabilities Act of 1990, 42 U.S.C. §12131 et seq., and its implementing regulations, 28 C.F.R. Part 35; as well as university policy 5-16. More information can be found at https://www.kent.edu/policyreg/administrative-policy-regarding-class-attendance-and-class-absence"
    currentSASText = "University policy 3-01.3 requires that students with disabilities be provided reasonable accommodations to ensure their equal access to course content.  If you have a documented disability and require accommodations, please contact the instructor at the beginning of the semester to make arrangements for necessary classroom adjustments.  Please note, you must   first verify your eligibility for these through Student Accessibility Services (contact 330-672-3391 or visit www.kent.edu/sas for more information on registration procedures)."
    currentRegistrationStatement = "The official registration deadline for this course can be found at https://www.kent.edu/registrar/calendars-deadlines. University policy requires all students to be officially registered in each class they are attending. Students who are not officially registered for a course by published deadlines should not be attending classes and will not receive credit or a grade for the course. Each student must confirm enrollment by checking his/her class schedule (using Student Tools in FlashLine) prior to the deadline indicated. Registration errors must be corrected prior to the deadline."
    

    # Non Key Columns
    attendance_policy = Column(String(500), nullable=True, default=currentAttendancePolicy)
    calender = Column(LargeBinary, nullable=True)
    # crn = Column(Integer, index)
    # TODO instroduction_statement(String(500), nullable=True)
    cheating_policy = Column(String(500), nullable=True) # TODO change name to optional cheating policy, maybe remove
    extra_policies = Column(String(500), nullable=True) # TODO change to 1000
    grading_policy = Column(String(500), nullable=True)
    meeting_dates = Column(String(100), nullable=True)
    meeting_time = Column(String(100), nullable=True)
    optional_materials = Column(String(256), nullable=True)
    pdf = Column(LargeBinary, nullable=True) # TODO set to longblob?
    required_materials = Column(String(256), nullable=True)
    # TODO registration_statement(String(600), default=currentRegistrationStatement)
    schedule = Column(LargeBinary, nullable=True)
    state = Column(Enum('approved', 'draft'), default='draft')
    Students_with_disabilities = Column(String(500), default=currentSASText) #TODO change to sastext
    University_cheating_policy = Column(String(500), 
                                        default=currentCheatingPolicy) # TODO set default to  default=currentCheatingPollicy
    withdrawl_date = Column(String(100), nullable=True)


    # TODO add building = Column(String(70)) 
    # TODO add room = Column(String(50))
    

    def addInstructor(self, instructor, job):
        '''Add an association between syllabus and instructor
        TODO: Test if this works flawlessly. Has not been tested

        Args: 
            instructor: Instructor - 
            job: String - 
        '''
        SyllabusInstructorAssociation.create(self, instructor, job)

    def setVersion(self):
        '''Sets the version number to one more than the previous
        
        select max(version)
        from syllabus
        where 'course_number = %'
              'course_version = %'
              'section = %'
              'semester = %'
              'year = %'
 
        '''
        conn = db.session.connection()
        meta = db.metadata
        syllabus = meta.tables['syllabus']
        print(self.semester)
        print(type(self.semester))
        s = select([db.func.max(syllabus.c.version)]) \
                .where(and_(syllabus.c.year == self.year,
                            syllabus.c.section == self.section, 
                            syllabus.c.course_version == self.course_version, 
                            syllabus.c.semester == self.semester,
                            syllabus.c.course_number == self.course_number))
        result = conn.execute(s)
        largestVersion = result.first().max_1
        if largestVersion:
            self.version = largestVersion + 1
            print(self.version)
        else:
            self.version = 1

    def setPDF(self):
        '''Generates a PDF document and sets self.pdf to it
        
        This function should be the final function called before comitting 
        to the DB. All other variables should be set when this function is called. 
        
        Args: 
            none. 
        
        Returns: 
            a success of failure message
        '''

        # Convert Model Data to HTML
        syllabusHTML = 'TODO' # = convertToHTML()

        # Convert HTML to PDF
        syllabusPDF = 'TODO' # = pdfKitFunction(syllabusHTML)

        self.pdf = syllabusPDF
        
        return 'failure'


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

def generateSyllabusVersion():
        x = Syllabus.query.filter_by(
                course_number=self.course_number,
                course_version=self.course_version,
                section=self.section,
                semester=self.semester,
                year=self.year)


class User(UserMixin, db.Model, Timestamp):
    '''User Model
    Relationship with Instructor
        one to one
    '''
    # Primary Keys
    email = Column(String(120), primary_key=True)

    # Foreign Keys
    instructor_id = Column(Integer, 
                           ForeignKey('instructor.id', 
                                      onupdate="CASCADE", 
                                      ondelete="SET NULL"),
                           nullable=True)

    # Relationships    
    instructor = relationship("Instructor", back_populates="user")

    # Non Key Columns
    password_hash = Column(String(128), nullable=False)
    permission = Column(Enum('admin', 'instructor'), nullable=False, 
                        server_default=text("instructor"))
    
    def get_id(self):
        '''Used for Flask-Login to get the primary key of User
        '''
        return (self.email)

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


