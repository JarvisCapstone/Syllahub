'''Creates fake models and adds them to the database. 

call commands like these from the flask shell
>>>TODO
'''
from app import db
from app.models import *
from sqlalchemy.sql.expression import func

from faker import Faker
from faker.providers import profile, phone_number, lorem, address, misc
import random
from abc import ABCMeta, abstractmethod
from typing import List, Set, Dict, Tuple, Optional

fake = Faker() 
fake.add_provider(profile)
fake.add_provider(phone_number)
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(address)


class Factory(metaclass=ABCMeta):
    @abstractmethod
    def getModel(self): 
        pass

    @abstractmethod
    def setData(self, temp, data): 
        pass

    def create(self, data=None):
        temp = self.getModel()
        tempData = data or {}
        temp = self.setData(temp, tempData)
        return temp

    def addToDB(self, num=None):
        num = num or 1
        u = self.create()
        db.session.add(u)
        db.session.commit()
        return "Success"


class UserFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return User()

    def setData(self, temp, data): 
        p = fake.simple_profile()
        if 'email' in data:
            temp.email = data.email
        else:
            temp.email = p['mail']

        if 'password' in data:
            temp.set_password(data.password)
        else:
            #password is 'password by default'
            temp.set_password('password')

        if 'permission' in data:
            temp.permission=data.permission
        
        if 'instructor_id' in data:
            temp.instructor_id=data.instructor_id

        return temp


class InstructorFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return Instructor()

    def setData(self, temp, data): 
        p = fake.simple_profile()
        if 'name' in data:
            temp.name=data.name
        else:
            temp.name=p['name']
        
        if 'phone' in data:
            temp.phone=data.phone
        else:
            temp.phone=random.randint(1000000000,9999999999)   

        if 'email' in data:
            temp.email=data.email
        else:
            temp.email=p['mail']

        
        if 'perfered_office_hours' in data:
            temp.perfered_office_hours=data.perfered_office_hours
        else:
            temp.perfered_office_hours='whenever'

        return temp


class CourseFactory(Factory):
    def __init__(self):
        Factory.__init__(self)

    def getModel(self):
        return Course()

    def setData(self, temp, data): 
        if 'number' in data:
            temp.number=data.number
        else:
            temp.number=fake.random_int(min=10000, max=99999)
        
        if 'version' in data:
            temp.version=data.version
        else:
            temp.version=fake.random_int(min=1, max=9)

        if 'name' in data:
            temp.name=data.name
        else:
            temp.name=fake.sentence(nb_words=3)

        if 'description' in data:
            temp.description=data.description
        else:
            temp.description=fake.paragraph(nb_sentences=2)

        if 'prerequisites' in data:
            temp.prerequisites=data.prerequisites
        else:
            temp.prerequisites=fake.sentence(nb_words=1)

        if 'building' in data:
            temp.building=data.building
        else:
            temp.building=fake.street_address()

        if 'room' in data:
            temp.room=data.room
        else:
            temp.room=fake.random_int(min=0, max=999)

        if 'is_core' in data:
            temp.is_core=data.is_core
        else:
            temp.is_core=fake.boolean(chance_of_getting_true=20)

        if 'is_wi' in data:
            temp.is_wi=data.is_wi
        else:
            temp.is_wi=fake.boolean(chance_of_getting_true=20)

        if 'is_elr' in data:
            temp.is_elr=data.is_elr
        else:
            temp.is_elr=fake.boolean(chance_of_getting_true=20)

        if 'is_diversity' in data:
            temp.is_diversity=data.is_diversity
        else:
            temp.is_diversity=fake.boolean(chance_of_getting_true=20)

        return temp


class CloFactory(Factory):
    def __init__(self):
        Factory.__init__(self)

    
    def getModel(self):
        return Clo()

    def setData(self, temp, data): 
        if 'general' in data:
            temp.general=data.general
        else:
            temp.general=fake.paragraph(nb_sentences=2)

        if 'specific' in data:
            temp.specific=data.specific
        else:
            temp.specific=fake.paragraph(nb_sentences=2)

        return temp


class SyllabusFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return Syllabus()

    def setData(self, temp, data): 
        #must reference a course. get a random course

        course = Course.query.order_by(func.rand()).first()

        u = Syllabus()
        if 'section' in data:
            temp.section = data.section
        else: 
            temp.section = fake.random_int(min=0, max=50)


        if 'semester' in data:
            temp.semester = data.semester
        else: 
            temp.semester = 'spring'


        if 'year' in data:
            temp.year = data.year
        else: 
            temp.year = 2018


        if 'version' in data:
            temp.version = data.version
        else: 
            temp.version = fake.random_int(min=1, max=9)


        if 'course_number' in data:
            temp.course_number = data.course_number
        else: 
            temp.course_number = course.number


        if 'course_version' in data:
            temp.course_version = data.course_version
        else: 
            temp.course_version = course.version


        if 'state' in data:
            temp.state = data.state
        else: 
            temp.state = 'draft'


        if 'pdf' in data:
            temp.pdf = data.pdf


        if 'calender' in data:
            temp.calender = data.calender


        if 'schedule' in data:
            temp.schedule = data.schedule


        if 'required_materials' in data:
            temp.required_materials = data.required_materials
        else: 
            temp.required_materials = fake.paragraph(nb_sentences=2)


        if 'optional_materials' in data:
            temp.optional_materials = data.optional_materials
        else: 
            temp.optional_materials = fake.paragraph(nb_sentences=2)


        if 'withdrawl_date' in data:
            temp.withdrawl_date = data.withdrawl_date
        else: 
            temp.withdrawl_date = fake.paragraph(nb_sentences=1)


        if 'grading_policy' in data:
            temp.grading_policy = data.grading_policy
        else: 
            temp.grading_policy = fake.paragraph(nb_sentences=3)


        if 'attendance_policy' in data:
            temp.attendance_policy = data.attendance_policy
        else: 
            temp.attendance_policy = fake.paragraph(nb_sentences=3)


        if 'cheating_policy' in data:
            temp.cheating_policy = data.cheating_policy
        else: 
            temp.cheating_policy = fake.paragraph(nb_sentences=3)


        if 'extra_policies' in data:
            temp.extra_policies = data.extra_policies
        else: 
            temp.extra_policies = fake.paragraph(nb_sentences=3)


        if 'meeting_time' in data:
            temp.meeting_time = data.meeting_time
        else: 
            temp.meeting_time = fake.paragraph(nb_sentences=1)


        if 'meeting_dates' in data:
            temp.meeting_dates = data.meeting_dates
        else: 
            temp.meeting_dates = fake.paragraph(nb_sentences=1)


        if 'University_cheating_policy' in data:
            temp.University_cheating_policy = data.University_cheating_policy
        else: 
            temp.University_cheating_policy = fake.paragraph(nb_sentences=3)


        if 'Students_with_disabilities' in data:
            temp.Students_with_disabilities = data.Students_with_disabilities
        else: 
            temp.Students_with_disabilities = fake.paragraph(nb_sentences=3)

        return temp



def createRandCloCourseAssociation():
    temp_course = Course.query.order_by(func.rand()).first()
    temp_clo = Clo.query.order_by(func.rand()).first()
    temp_course.clos.append(temp_clo)
    db.session.commit()


def createRandInstructorSyllabusAssociation():
    temp_syllabus = Syllabus.query.order_by(func.rand()).first()
    temp_instructor = Instructor.query.order_by(func.rand()).first()
    SyllabusInstructorAssociation.create2(temp_syllabus, temp_instructor, 'grader')


def generateData(num=None):
    '''seed db with junk data
    Warning: does not check for primary keys. 
    may randomly create2 existing data and crash
    '''
    if not num: 
        num = 3
    else:
        num = int(num)

    factories = []
    factories.append(UserFactory())
    factories.append(InstructorFactory())
    factories.append(CourseFactory())
    factories.append(CloFactory())
    factories.append(SyllabusFactory())
    print(factories)
    for factory in factories:
        factory.addToDB(num)

    print("added", num, "fake data entries to each table in db")