from fpdf import FPDF
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
        # test if already exists
        
        sia = SyllabusInstructorAssociation.query.filter_by(
                  syllabus_course_number = syllabus.course_number,
                  syllabus_course_version = syllabus.course_version,
                  syllabus_section = syllabus.section,
                  syllabus_semester = syllabus.semester,
                  syllabus_version = syllabus.version,
                  syllabus_year = syllabus.year,
                  instructor_id = instructor.id).first()
        #print('sia=', sia)
        if not sia:
            new_job = SyllabusInstructorAssociation(job_on_syllabus=job)
            new_job.instructor = instructor;
            new_job.syllabus = syllabus;
            db.session.add(new_job)
            db.session.commit()

            #update syllabus pdf
            syllabus.setPDF()
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

    def setVersion(self):
        '''Sets the version number to one more than the previous
        '''
        conn = db.session.connection()
        meta = db.metadata
        course = meta.tables['course']
        s = select([db.func.max(course.c.version)]) \
                .where(and_(course.c.number == self.number))
        result = conn.execute(s)
        largestVersion = result.first().max_1
        if largestVersion:
            print('largest')
            self.version = largestVersion + 1
        else:
            print('else')
            self.version = 1
        print('self.version', self.version)


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


    def updateIfDifferent(self, data):
        '''change any data in instructor if it differs from data
        Does not update any relationships

        Args:
            data 
                a dictionary object that should contain values in the id 
                or email keys. This is because id and email are the only fields
                that can uniquely identify an instructor
        '''

        changed = False

        if 'email' in data:
            if not self.email == data['email']:
                self.email = data['email']
                changed =  True 
        
        if 'name' in data:
            if not self.name == data['name']:
                self.name = data['name']
                changed =  True 
        
        if 'perfered_office_hours' in data:
            if not self.perfered_office_hours == data['perfered_office_hours']:
                self.perfered_office_hours = data['perfered_office_hours']
                changed =  True 
        
        if 'phone' in data:
            if not self.phone == data['phone']:
                self.phone = data['phone']
        
        if changed:
            db.session.commit()



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
    version = Column(Integer, primary_key=True)

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
        pdf=FPDF()

        course=Course.query.filter_by(number=self.course_number,
                                    version=self.course_version).first()

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 5, 'CS' + str(self.course_number) + ' ' + course.name, ln=1, align='C')
        pdf.cell(0, 5, 'Course Syllabus', ln=1, align='C')
        pdf.ln(5)
        
        pdf.set_font_size(14)
        for instructor in self.instructorList:
            pdf.cell(0, 10, instructor.name, ln=1, align='C')
        pdf.ln(5)
        pdf.set_font('')
        pdf.cell(0, 5, self.semester + ' ' + str(self.year) + ' Semester', ln=1, align='C')
        #TODO, make section number a string in database, add check
        # for section to determine campus
        pdf.cell(0, 5, 'Kent Campus, Section: ' + str(self.section), ln=1, align='C')
        #TODO, fix once room number and building are moved to syllabus
        #TODO, revamp meeting_time once we get delimiter solved
        if self.meeting_time and course.room and course.building:
            pdf.cell(0, 5, self.meeting_time + ', ' +
                str(course.room) + ' ' + course.building , ln=1, align='C')
        else:
            pdf.cell(0, 10, 'This is an online course, there is no meeting times',
                    ln=1, align='C')
        pdf.ln(10)

        #TODO, optional, once in db
        #if introduction != null:
            #pdf.set_font_size(14)
            #pdf.cell(0,5, 'Instructor Introduction', ln=1)
            #pdf.set_font_size(12)
            #pdf.multi_cell(0,5, 'Walker is a very nice man who is teaching this course')
            #pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Contact Information', ln=1)
        pdf.set_font_size(12)
        for instructor in self.instructorList:
            pdf.cell(0,5, 'Email: ' + instructor.email, ln=1)
            pdf.cell(0,5, 'Phone: ' + str(instructor.phone), ln=1)
            #TODO, include office room in database, nevermind  have it included in office hours
            #pdf.cell(0,5, 'Office: #####', ln=1)
            if instructor.perfered_office_hours:
                pdf.cell(0,5, 'Office Hours: ' + instructor.perfered_office_hours, ln=1)
                pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Course Description from the University Catalog', ln=1)
        pdf.set_font_size(12)
        if course.description:
            pdf.multi_cell(0,5, 'CS'+str(self.course_number) + ' ' + course.name + ': ' +
                           course.description)
        else:
            pdf.multi_cell(0,5, 'CS'+str(self.course_number) + ' ' + course.name + ': ')
        if (course.prerequisites != None):
            pdf.cell(0,5, 'Prerequisite: ' + course.prerequisites, ln=1)
            pdf.cell(0, 5, 'Students without the proper prerequisite(s) risk being deregistered from the class', ln=1)
        pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Course Learning Outcomes', ln=1)
        pdf.set_font_size(12)
        pdf.cell(0,5, 'By the end of this course, you should be able to:', ln=1)
        for clo in course.clos:
            pdf.multi_cell(0,5, clo.general)
        pdf.ln(5)

        if(course.is_core):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This coourse may be used to satisfy a Kent Core requirement. The Kent Core as a whole is intended to broaden intellectual perspectives, foster ethical and humanitarian values, and prepare students for responsible citizenship and productive careers.')
        if(course.is_diversity==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to satisfy the University Diversity requirement. Diversity courses provide opportunities for students to learn about such matters as the history, culture, values and notable achievements of people other than those of their own national origin, ethnicity, religion, sexual orientaiton, age, gender, physical and mental ability, and social class. Diversity courses also provide opportunities to examine problems and issues that may arise from differences, and opportunities to learn how to deal constructively with them.')
        if(course.is_wi==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to satisfy the Writing Intensive Course (WIC) requirement. The purpose of a writing-intensive course is to assist students in becoming effective writers within their major discipline. A WIC requires a substantial amount of writing, provides opportunities for guided revision, and focuses on writing forms and standards used in the professional life of the discipline.')
        if(course.is_elr==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to fulfill the university\'s Experiential Learning Requirement (ELR) which provides students with the opportunity to initiate lifelong learning through the development and application of academic knowledge and skills in new or different settings. Experiential learning can occur through civic engagement, creative and artistic activities, practical experiences, research, and study abroad/away.')
        
        #TODO, required should be moved to course, no syllabus
        if (self.required_materials != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Required Materials', ln=1)
            pdf.set_font_size(12)
            pdf.multi_cell(0,5, self.required_materials)
        if (self.optional_materials != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Optional Materials', ln=1)
            pdf.set_font_size(12)
            pdf.cell(0,5, self.optional_materials, ln=1)

        #TODO, enforce notnull dates / policies
        if (self.grading_policy != None):   
            pdf.ln(5)        
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Grading Policy', ln=1)
            pdf.multi_cell(0,5, self.grading_policy)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Registration Date', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, 'University policy requires all students to be officially registered in each class they are attending. Students who are not officially registered for a course by published deadlines should not be attending classes and will not receive credit or a grade for the course. Each student must confirm enrollment by checking his/her class schedule (using Student Tools in FlashLine) prior to the deadline indicated. Registration errors must be corrected prior to the deadline.')
        pdf.cell(0,5, 'https://www.kent.edu/registrar/fall-your-time-register', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Withdrawl Date', ln=1)
        pdf.set_font_size(12)
        pdf.cell(0, 5, 'The course withdrawal deadline is found below', ln=1)
        pdf.cell(0,5, 'https://www.kent.edu/registrar/spring-important-dates', ln=1)

        pdf.ln(5)
        
        if self.attendance_policy:
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Attendance Policy', ln=1)
            pdf.set_font_size(12)
            pdf.multi_cell(0,5, self.attendance_policy)
            pdf.ln(5)
        #pdf.cell(0,5, 'Attendance Policy goes here', ln=1)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Student Accessability Services', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, self.Students_with_disabilities)
        #pdf.cell(0,5, 'Important info here', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Academic Integrity', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, self.cheating_policy)
        #pdf.cell(0,5, "Don't plagarize bad", ln=1)

        if (self.extra_policies != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Extra Policies', ln=1)
            pdf.set_font_size(12)
            pdf.multi_cell(0,5, self.extra_policies)
        

        #pdf.output('course.pdf', 'F')

        # Convert Model Data to HTML
        #syllabusHTML = 'TODO' # = convertToHTML()

        # Convert HTML to PDF
        #syllabusPDF = 'TODO' # = pdfKitFunction(syllabusHTML)

        self.pdf = pdf.output(dest='S').encode('latin-1')
        #pdf.output('wolves.pdf', 'F')
        #file = open('wolves.pdf', 'rb').read()
        #self.pdf = file
        #db.session.query(Syllabus) \
            #.filter_by(self) \
            #.update({"pdf": (file)})
        #db.session.commit()

        if(self.pdf != None):
            return 'success'
        else:
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


