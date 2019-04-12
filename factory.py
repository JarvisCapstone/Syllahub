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
        num = int(num) or 1
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
        Factory.__init__(self, Clo)

    
    def getModel(self):
        return Clo()

    def create2(general=None, specific=None):
        u = Clo()

        u.general = general or fake.paragraph(nb_sentences=2)
        u.specific = specific or fake.paragraph(nb_sentences=2)

        return u



class SyllabusFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return Syllabus()

    def create2(section=None, semester=None, year=None, version=None, 
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
        u.section = section or fake.random_int(min=0, max=50)
        u.semester = semester or 'spring'
        u.year = year or 2018
        u.version = version or fake.random_int(min=1, max=9)
        u.course_number = course_number or course.number
        u.course_version = course_version or course.version
        u.state = state or 'draft'

        if pdf:
            u.pdf = pdf

        if calender:
            u.calender = calender

        if schedule:
            u.schedule = schedule

        u.required_materials = required_materials or fake.paragraph(nb_sentences=2)
        u.optional_materials = optional_materials or fake.paragraph(nb_sentences=2)
        u.withdrawl_date = withdrawl_date or fake.paragraph(nb_sentences=1)
        u.grading_policy = grading_policy or fake.paragraph(nb_sentences=3)
        u.attendance_policy = attendance_policy or fake.paragraph(nb_sentences=3)
        u.cheating_policy = cheating_policy or fake.paragraph(nb_sentences=3)
        u.extra_policies = extra_policies or fake.paragraph(nb_sentences=3)
        u.meeting_time = meeting_time or fake.paragraph(nb_sentences=1)
        u.meeting_dates = meeting_dates or fake.paragraph(nb_sentences=1)
        u.University_cheating_policy = University_cheating_policy or fake.paragraph(nb_sentences=3)
        u.Students_with_disabilities = Students_with_disabilities or fake.paragraph(nb_sentences=3)

        return u



def create2RandCloCourseAssociation():
    temp_course = Course.query.order_by(func.rand()).first()
    temp_clo = Clo.query.order_by(func.rand()).first()
    temp_course.clos.append(temp_clo)
    db.session.commit()


def create2RandInstructorSyllabusAssociation():
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
    u = UserFactory()
    factories.append(u)
    print(factories)
    for factory in factories:
        x = factory.create()
        print("generated x=", x)
    '''
    for x in range(num):
        addFakeCourseToDB()
        addFakeInstructorToDB()
        addFakeUserToDB()
        addFakeCloToDB()
        addFakeSyllabusToDB()
        create2RandCloCourseAssociation()
        create2RandInstructorSyllabusAssociation()
    '''
    print("added", num, "fake data entries to each table in db")