'''creates fake models and adds them to the database. 

call commands like these from the flask shell
>>>factory.addFakeUserToDB()

'''
from app import db
from app.models import *
from sqlalchemy.sql.expression import func

from faker import Faker
from faker.providers import profile, phone_number, lorem, address, misc
import random

fake = Faker() 
fake.add_provider(profile)
fake.add_provider(phone_number)
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(address)


class Factory:
    def __init__(self, model):
        self.model = model
        self.data = []

    def setDefaultData():
        pass

    def create():
        pass

    def addToDB(num=None):
        if not num: 
            num = 3
        else:
            num = int(num)
        return "TODO"


class UserFactory(Factory):
    def __init__(self):
        Factory.__init__(self, User)


def createFakeUser(username=None, email=None, password=None, permission=None, instructor_id=None):
    p = fake.simple_profile()
    u = User()
    if username:
        u.username=username
    else:
        u.username=p['username']
    
    if email:
        u.email=email
    else:
        u.email=p['mail']    
    
    if password:
        u.set_password(password)
    else:
        #password is 'password by default'
        u.set_password('password')

    if permission:
        u.permission=permission
    
    if instructor_id:
        u.instructor_id=instructor_id

    return u

def addFakeUserToDB(username=None, email=None, password=None, permission=None, instructor_id=None):
    u = createFakeUser(username, email, password, permission, instructor_id)
    db.session.add(u)
    db.session.commit()



def createFakeInstructor(name=None, phone=None, email=None, perfered_office_hours=None):
    p = fake.simple_profile()
    u = Instructor()
    if name:
        u.name=name
    else:
        u.name=p['name']
    
    if phone:
        u.phone=phone
    else:
        u.phone=random.randint(1000000000,9999999999)   

    if email:
        u.email=email
    else:
        u.email=p['mail']

    
    if perfered_office_hours:
        u.perfered_office_hours=perfered_office_hours
    else:
        u.perfered_office_hours='whenever'

    return u

def addFakeInstructorToDB(name=None, phone=None, email=None, perfered_office_hours=None):
    u = createFakeInstructor(name, phone, email, perfered_office_hours)
    db.session.add(u)
    db.session.commit()



def createFakeCourse(number=None, version=None, name=None, description=None, 
                     prerequisites=None, building=None, room=None, 
                     is_core=None, is_wi=None, is_elr=None, is_diversity=None):   
    u = Course()
    if number:
        u.number=number
    else:
        u.number=fake.random_int(min=10000, max=99999)
    
    if version:
        u.version=version
    else:
        u.version=fake.random_int(min=1, max=9)

    if name:
        u.name=name
    else:
        u.name=fake.sentence(nb_words=3)

    if description:
        u.description=description
    else:
        u.description=fake.paragraph(nb_sentences=2)

    if prerequisites:
        u.prerequisites=prerequisites
    else:
        u.prerequisites=fake.sentence(nb_words=1)

    if building:
        u.building=building
    else:
        u.building=fake.street_address()

    if room:
        u.room=room
    else:
        u.room=fake.random_int(min=0, max=999)

    if is_core:
        u.is_core=is_core
    else:
        u.is_core=fake.boolean(chance_of_getting_true=20)

    if is_wi:
        u.is_wi=is_wi
    else:
        u.is_wi=fake.boolean(chance_of_getting_true=20)

    if is_elr:
        u.is_elr=is_elr
    else:
        u.is_elr=fake.boolean(chance_of_getting_true=20)

    if is_diversity:
        u.is_diversity=is_diversity
    else:
        u.is_diversity=fake.boolean(chance_of_getting_true=20)

    return u

def addFakeCourseToDB(number=None, version=None, name=None, description=None, 
                     prerequisites=None, building=None, room=None, 
                     is_core=None, is_wi=None, is_elr=None, is_diversity=None):
    u = createFakeCourse(number, version, name, description, 
                         prerequisites, building, room, 
                         is_core, is_wi, is_elr, is_diversity)
    db.session.add(u)
    db.session.commit()



def createFakeClo(general=None, specific=None):
    u = Clo()

    if general:
        u.general=general
    else:
        u.general=fake.paragraph(nb_sentences=2)

    if specific:
        u.specific=specific
    else:
        u.specific=fake.paragraph(nb_sentences=2)

    return u

def addFakeCloToDB(general=None, specific=None): 
    u = createFakeClo(general, specific)
    db.session.add(u)
    db.session.commit()



def createFakeSyllabus(section=None, semester=None, year=None, version=None, 
                       course_number=None, course_version=None, state=None, 
                       pdf=None, calender=None, schedule=None, 
                       required_materials=None, optional_materials=None, 
                       withdrawl_date=None, grading_policy=None, 
                       attendance_policy=None, cheating_policy=None, 
                       extra_policies=None, meeting_time=None, 
                       meeting_dates=None, University_cheating_policy=None, 
                       Students_with_disabilities=None):
    #must reference a course. get a random course

    course = Course.query.order_by(func.rand()).first()

    u = Syllabus()
    if section:
        u.section = section
    else: 
        u.section = fake.random_int(min=0, max=50)


    if semester:
        u.semester = semester
    else: 
        u.semester = 'spring'


    if year:
        u.year = year
    else: 
        u.year = 2018


    if version:
        u.version = version
    else: 
        u.version = fake.random_int(min=1, max=9)


    if course_number:
        u.course_number = course_number
    else: 
        u.course_number = course.number


    if course_version:
        u.course_version = course_version
    else: 
        u.course_version = course.version


    if state:
        u.state = state
    else: 
        u.state = 'draft'


    if pdf:
        u.pdf = pdf


    if calender:
        u.calender = calender


    if schedule:
        u.schedule = schedule


    if required_materials:
        u.required_materials = required_materials
    else: 
        u.required_materials = fake.paragraph(nb_sentences=2)


    if optional_materials:
        u.optional_materials = optional_materials
    else: 
        u.optional_materials = fake.paragraph(nb_sentences=2)


    if withdrawl_date:
        u.withdrawl_date = withdrawl_date
    else: 
        u.withdrawl_date = fake.paragraph(nb_sentences=1)


    if grading_policy:
        u.grading_policy = grading_policy
    else: 
        u.grading_policy = fake.paragraph(nb_sentences=3)


    if attendance_policy:
        u.attendance_policy = attendance_policy
    else: 
        u.attendance_policy = fake.paragraph(nb_sentences=3)


    if cheating_policy:
        u.cheating_policy = cheating_policy
    else: 
        u.cheating_policy = fake.paragraph(nb_sentences=3)


    if extra_policies:
        u.extra_policies = extra_policies
    else: 
        u.extra_policies = fake.paragraph(nb_sentences=3)


    if meeting_time:
        u.meeting_time = meeting_time
    else: 
        u.meeting_time = fake.paragraph(nb_sentences=1)


    if meeting_dates:
        u.meeting_dates = meeting_dates
    else: 
        u.meeting_dates = fake.paragraph(nb_sentences=1)


    if University_cheating_policy:
        u.University_cheating_policy = University_cheating_policy
    else: 
        u.University_cheating_policy = fake.paragraph(nb_sentences=3)


    if Students_with_disabilities:
        u.Students_with_disabilities = Students_with_disabilities
    else: 
        u.Students_with_disabilities = fake.paragraph(nb_sentences=3)

    return u

def addFakeSyllabusToDB(section=None, semester=None, year=None, version=None, 
                        course_number=None, course_version=None, state=None, 
                        pdf=None, calender=None, schedule=None, 
                        required_materials=None, optional_materials=None, 
                        withdrawl_date=None, grading_policy=None, 
                        attendance_policy=None, cheating_policy=None, 
                        extra_policies=None, meeting_time=None, 
                        meeting_dates=None, University_cheating_policy=None, 
                        Students_with_disabilities=None): 
    u = createFakeSyllabus(section, semester, year, version, course_number, 
                           course_version, state, pdf, calender, schedule, 
                           required_materials, optional_materials, 
                           withdrawl_date, grading_policy, attendance_policy, 
                           cheating_policy, extra_policies, meeting_time, 
                           meeting_dates, University_cheating_policy, 
                           Students_with_disabilities)
    db.session.add(u)
    db.session.commit()


def createRandCloCourseAssociation():
    temp_course = Course.query.order_by(func.rand()).first()
    temp_clo = Clo.query.order_by(func.rand()).first()
    temp_course.clos.append(temp_clo)
    db.session.commit()


def printRandInstructorSyllabi():
    i = Instructor.query.filter_by(id=18).first()
    print(i.syllabiList)
    print(i.all_syllabus_associations)
    #s = Instructor.query.filter_by(id=18).first()
    #print(s.syllabiList)

def printRandSyllabusInstructors():
    temp_syllabus = Syllabus.query.order_by(func.rand()).first()
    print(temp_syllabus.instructorList)
    print(temp_syllabus.all_instructor_associations)
    #s = Instructor.query.filter_by(id=18).first()
    #print(s.syllabiList)

def createRandInstructorSyllabusAssociation():
    temp_syllabus = Syllabus.query.order_by(func.rand()).first()
    temp_instructor = Instructor.query.order_by(func.rand()).first()
    temp_job = SyllabusInstructorAssociation(job_on_syllabus='teacher')
    temp_job.instructor = temp_instructor;
    temp_job.syllabus = temp_syllabus;
    db.session.add(temp_job)
    db.session.commit()


def generateData(num=None):
    '''seed db with junk data
    Warning: does not check for primary keys. 
    may randomly create existing data and crash
    '''
    if not num: 
        num = 3
    else:
        num = int(num)

    for x in range(num):
        addFakeCourseToDB()
        addFakeInstructorToDB()
        addFakeUserToDB()
        addFakeCloToDB()
        addFakeSyllabusToDB()
        createRandCloCourseAssociation()
        createRandInstructorSyllabusAssociation()

    print("added", num, "fake data entries to each table in db")