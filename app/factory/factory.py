'''Creates fake models and adds them to the database. 
'''
import pprint
from app import db
from app.models import *
from sqlalchemy.sql.expression import func
from flask import flash
from flask_login import current_user

from faker import Faker
from faker.providers import profile, phone_number, lorem, address, misc
import random
from abc import ABCMeta, abstractmethod
from typing import List, Set, Dict, Tuple, Optional


class Factory(metaclass=ABCMeta):
    def __init__(self):
        self.fake.add_provider(profile)
        self.fake.add_provider(phone_number)
        self.fake.add_provider(lorem)
        self.fake.add_provider(misc)
        self.fake.add_provider(address)

    fake = Faker()

    @abstractmethod
    def getModel(self): 
        pass

    @abstractmethod
    def setData(self, temp, data): 
        pass

    @abstractmethod
    def deleteAll(showFlashMessage=True): 
        pass

    @abstractmethod
    def getFakeData(self): 
        pass

    def create(self, data):
        temp = self.getModel()
        temp = self.setData(temp, data)
        db.session.add(temp)
        db.session.commit()
        return temp

    def createFakes(self, num=None):
        num = num or 1
        for i in range(num):
            data = self.getFakeData()
            self.create(data)
        return "Success"


class UserFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return User()

    def getFakeData(self): 
        data={}
        p = self.fake.simple_profile()
        data['email'] = p['mail']
        data['password'] = 'password'
        #data.permission=
        #data.instructor_id=data.instructor_id

        return data

    def setData(self, temp, data): 
        temp.email = data['email']
        temp.set_password(data['password'])
        if 'permission' in data:
            temp.permission=data['permission']
        if 'instructor_id' in data:
            temp.instructor_id=data['instructor_id']

        return temp

    def createAdmin(self):
        '''Adds admin@syllahub.com to db if it isn't already there
        '''
        adminEmail='syllahub@gmail.com'
        
        data = {}
        data['email'] = adminEmail
        data['password'] = 'admin'
        data['permission'] = 'admin'

        admin = User.query.filter_by(email=adminEmail).first()
        if admin is None:
            self.create(data)
            #admin = User(email=adminEmail)
            #admin.set_password('admin')
            #db.session.add(admin)
            #db.session.commit()
            return 'Generated ' + adminEmail
        elif not admin.permission =='admin':
            admin.permission='admin'
            db.session.commit()
            return 'Set ' + adminEmail + ' to an admin'
        else:
            return adminEmail + ' is already an admin in the database'

    def deleteAll(showFlashMessage=True):
        '''Deletes all users except the Currently logged in user. 
        '''
        num = db.session.query(User).filter(User.email != current_user.email) \
                  .delete(synchronize_session=False)
        db.session.commit()
        if showFlashMessage:
            flash("Deleted {} Users".format(num))


class InstructorFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return Instructor()

    def getFakeData(self): 
        data={}
        p = self.fake.simple_profile()
        data['name'] = p['name']
        data['phone'] = random.randint(1000000000,9999999999)   
        data['email'] = p['mail']
        data['perfered_office_hours'] = 'whenever'

        return data

    def setData(self, temp, data): 
        if 'name' in data:
            temp.name=data['name']
        if 'phone' in data:
            temp.phone=data['phone']
        if 'email' in data:
            temp.email=data['email']
        if 'perfered_office_hours' in data:
            temp.perfered_office_hours=data['perfered_office_hours']
        return temp

    def deleteAll(showFlashMessage=True):
        num = db.session.query(Instructor).delete()
        db.session.commit()
        if showFlashMessage:
            flash("Deleted {} Instructors".format(num))


class CourseFactory(Factory):
    def __init__(self):
        Factory.__init__(self)

    def getModel(self):
        return Course()

    def getFakeData(self): 
        data={}
        data['number'] = self.fake.random_int(min=10000, max=99999)
        data['version'] = self.fake.random_int(min=1, max=9)
        data['name'] = self.fake.sentence(nb_words=3)
        data['description'] = self.fake.paragraph(nb_sentences=2)
        data['prerequisites'] = self.fake.sentence(nb_words=1)
        data['building'] = self.fake.street_address()
        data['room'] = self.fake.random_int(min=0, max=999)
        data['is_core'] = self.fake.boolean(chance_of_getting_true=20)
        data['is_wi'] = self.fake.boolean(chance_of_getting_true=20)
        data['is_elr'] = self.fake.boolean(chance_of_getting_true=20)
        data['is_diversity'] = self.fake.boolean(chance_of_getting_true=20)

        return data

    def setData(self, temp, data): 
        if 'number' in data:
            temp.number = data['number']
        if 'version' in data:
            temp.version = data['version']
        if 'name' in data:
            temp.name = data['name']
        if 'description' in data:
            temp.description = data['description']
        if 'prerequisites' in data:
            temp.prerequisites = data['prerequisites']
        if 'building' in data:
            temp.building = data['building']
        if 'room' in data:
            temp.room = data['room']
        if 'is_core' in data:
            temp.is_core = data['is_core']
        if 'is_wi' in data:
            temp.is_wi = data['is_wi']
        if 'is_elr' in data:
            temp.is_elr = data['is_elr']
        if 'is_diversity' in data:
            temp.is_diversity = data['is_diversity']
        return temp

    def createOrGet(number, version=None, name=None):
        '''Given a number [and version], get or create course with that pk
        '''
        course = None
        if version == 'any':
            existingCourseList = Course.query.filter_by(number=number).all()
            #print('existingCourseList', existingCourseList)
            if len(existingCourseList) == 0:
                newCourse = Course()
                newCourse.number = number
                newCourse.version = 1 #TODO, remove once autoincrement is changed
                db.session.add(newCourse)
                db.session.commit()
                course = newCourse
                #print('new course added')
            else:
                # search course list for most recent version
                # TODO
                #print('course already exists')
                course = existingCourseList[0] # TODO, fix this
            #print(course)

        else:
            course = Course.query.filter_by(number=number, version=version).first()
        #print('course=', course)
        return course

    def updateIfDifferent(course, name=None):
        '''TODO add more fields other than name
        '''
        # For each item, check if the existing course needs updating. 
        # if so, update and save to db
        changed = False
        if name:
            if not course.name == name:
                course.name = name
                changed = True

        if changed:
            db.session.commit()
                #print('name=', newCourse.name)
        # TODO, figure out how we will do time and loc information
        #locationList = r.Loc
        #BuildingStr = ""
        #timeStr = 
        #for location in locationList
        #    locationStr += location

    def deleteAll(showFlashMessage=True):
        num = db.session.query(Course).delete()
        db.session.commit()
        if showFlashMessage:
            flash("Deleted {} Courses ".format(num))


class CloFactory(Factory):
    def __init__(self):
        Factory.__init__(self)

    def getModel(self):
        return Clo()

    def getFakeData(self): 
        data={}
        data['general'] = self.fake.paragraph(nb_sentences=2)
        data['specific'] = self.fake.paragraph(nb_sentences=2)

        return data

    def setData(self, temp, data): 
        if 'general' in data:
            temp.general = data['general']
        
        if 'specific' in data:
            temp.specific = data['specific']
        
        return temp

    def deleteAll(showFlashMessage=True):
        num = db.session.query(Clo).delete()
        db.session.commit()
        if showFlashMessage:
            flash("Deleted {} CLO's".format(num))


class SyllabusFactory(Factory):
    def __init__(self):
        Factory.__init__(self)
    
    def getModel(self):
        return Syllabus()

    def getFakeData(self): 
        data={}
        course = Course.query.order_by(func.rand()).first()
        #course = Course.query.filter_by(number=96260).first()
        #print
        if course is None:
            raise Exception("There are no courses")
    
        data['section'] = self.fake.random_int(min=0, max=2)
        data['semester'] = 'spring'
        data['year'] = 2018
        data['course_number'] = course.number
        data['course_version'] = course.version
        data['state'] = 'draft'
        data['required_materials'] = self.fake.paragraph(nb_sentences=2)
        data['optional_materials'] = self.fake.paragraph(nb_sentences=2)
        data['withdrawl_date'] = self.fake.paragraph(nb_sentences=1)
        data['grading_policy'] = self.fake.paragraph(nb_sentences=3)
        #data['attendance_policy'] = self.fake.paragraph(nb_sentences=3)
        data['cheating_policy'] = self.fake.paragraph(nb_sentences=3)
        data['extra_policies'] = self.fake.paragraph(nb_sentences=3)
        data['meeting_time'] = self.fake.paragraph(nb_sentences=1)
        data['meeting_dates'] = self.fake.paragraph(nb_sentences=1)
        #data['University_cheating_policy'] = self.fake.paragraph(nb_sentences=3)
        #data['Students_with_disabilities'] = self.fake.paragraph(nb_sentences=3)

        return data

    def setData(self, temp, data): 
        #must reference a course. get a random course
        print('setData called')
        course = Course.query.filter_by(number=data['course_number'], 
                                        version=data['course_version']).first()
        if course is None:
            raise Exception("The course does not exist")
        u = Syllabus()
        if 'section' in data:
            temp.section = data['section']
        if 'semester' in data:
            temp.semester = data['semester']
        if 'year' in data:
            temp.year = data['year']

        if 'course_number' in data:
            temp.course_number = data['course_number']
        if 'course_version' in data:
            temp.course_version = data['course_version']
        
        # version is generated with this function
        temp.setVersion()

        if 'state' in data:
            temp.state = data['state']
        #if 'pdf' in data:
        #    temp.pdf = data['pdf']
        if 'calender' in data:
            temp.calender = data['calender']
        if 'schedule' in data:
            temp.schedule = data['schedule']
        if 'required_materials' in data:
            temp.required_materials = data['required_materials']
        if 'optional_materials' in data:
            temp.optional_materials = data['optional_materials']
        if 'withdrawl_date' in data:
            temp.withdrawl_date = data['withdrawl_date']
        if 'grading_policy' in data:
            temp.grading_policy = data['grading_policy']
        if 'attendance_policy' in data:
            temp.attendance_policy = data['attendance_policy']
        if 'cheating_policy' in data:
            temp.cheating_policy = data['cheating_policy']
        else:
            temp.cheating_policy = Syllabus.currentCheatingPolicy
        if 'extra_policies' in data:
            temp.extra_policies = data['extra_policies']
        if 'meeting_time' in data:
            temp.meeting_time = data['meeting_time']
        if 'meeting_dates' in data:
            temp.meeting_dates = data['meeting_dates']
        if 'University_cheating_policy' in data:
            temp.University_cheating_policy = data['University_cheating_policy']
        if 'Students_with_disabilities' in data:
            temp.Students_with_disabilities = data['Students_with_disabilities']
        else:
            # must set before database commit so pdf can be generated
            temp.Students_with_disabilities = Syllabus.currentSASText 
        temp.setPDF()
        return temp

    def createOrGet(self, course_number, course_version, section, semester, year, version=None):
        '''Provided the pk, get a syllabus if it exists, or create one if not
        '''
        syllabus = None
        if version == 'any':
            existingSyllabusList = Syllabus.query.filter_by(
                course_number=course_number,
                course_version=course_version,
                section=section,
                semester=semester,
                year=year).all()

            if len(existingSyllabusList) == 0:
                data = {}
                data['section'] = section
                data['semester'] = semester
                data['year'] = year
                data['course_number'] = course_number
                data['course_version'] = course_version

                #newSyllabus = Syllabus()
                #newSyllabus.course_number = course_number
                #newSyllabus.course_version = course_version
                #newSyllabus.version = 1 #TODO, remove once autoincrement is changed
                #newSyllabus.section = section
                #newSyllabus.semester = semester
                #newSyllabus.year = year
               
                #db.session.add(newSyllabus)
                #db.session.commit()
                #syllabus = newSyllabus
                syllabus = self.create(data)
                #print('new syllabus added')
            else:
                # search course list for most recent version
                # TODO
                # For each item, check if the existing course needs updating. 
                # if so, update and save to db
                #print('syllabus already exists')
                syllabus = existingSyllabusList[0] # TODO, fix this

        else:
            syllabus = Syllabus.query.filter_by(course_number=course.number,
                                                course_version=course.version,
                                                section=section,
                                                semester=semester,
                                                year=year).first()
        #print('syllabus=', syllabus)
        return syllabus

    def updateIfDifferent(syllabus, meeting_time=None):
        '''TODO add more fields other than meeting_time
        '''
        # For each item, check if the existing syllabus needs updating. 
        # if so, update and save to db
        changed = False
        if meeting_time:
            if not syllabus.meeting_time == meeting_time:
                syllabus.meeting_time = meeting_time
                changed = True

        if changed:
            db.session.commit()
                #print('name=', newCourse.name)
        # TODO, figure out how we will do time and loc information
        #locationList = r.Loc
        #BuildingStr = ""
        #timeStr = 
        #for location in locationList
        #    locationStr += location

    def deleteAll(showFlashMessage=True):
        #num = Syllabus.query().delete()
        num = db.session.query(Syllabus).delete()
        db.session.commit()
        if showFlashMessage:
            flash("Deleted {} Syllabi".format(num))


def createRandCloCourseAssociation():
    temp_course = Course.query.order_by(func.rand()).first()
    temp_clo = Clo.query.order_by(func.rand()).first()
    temp_course.clos.append(temp_clo)
    db.session.commit()


def createRandInstructorSyllabusAssociation():
    temp_syllabus = Syllabus.query.order_by(func.rand()).first()
    #temp_instructor = Instructor.query.order_by(func.rand()).first()
    temp_instructor = Instructor.query.filter_by(id=36).first()
    SyllabusInstructorAssociation.create(temp_syllabus, temp_instructor, 'grader')


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
    #print(factories)
    for factory in factories:
        factory.createFakes(num)

    flash("added", num, "fake data entries to each table in db")