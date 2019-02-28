from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #permission = db.Column(db.Integer, default=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    


class Syllabus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    #course_id = db.Column(db.Integer, foreign_key=True)
    #required_materials = db.Column(db.String(256))
    #pdf = db.Column(???)
    #optional_materials = db.Column(???)
    #calender = db.Column(???)
    #withdrawl = db.Column(???)
    #schedule = db.Column(???)
    #grading_policy = db.Column(???)
    #attendance_policy = db.Column(???)
    #cheating_policy = db.Column(???)
    #extra_policies = db.Column(???)
    #meeting_time = db.Column(???)
    #meeting_dates = db.Column(???)
    #static_information_version_id = db.Column(???)
    #timestamp = db.Column(???)
    

class SyllabusStaticInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    #cheating_policy = db.Column(???)
    #students_with_disabilities = db.Column(???)
    

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    crn = db.Column(db.Integer)
    description = db.Column(db.String(256))
    #description = db.Column(db.String(256))
    #is_core = db.Column(db.Integer)
    #is_wic = db.Column(db.Integer)
    #is_elr = db.Column(db.Integer)
    #is_diversity = db.Column(db.Integer)
    #prerequisites = db.Column(db.String(256))
    
class CLO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), unique=True)
    #permission = db.Column(db.Integer, default=1)


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    #perfered_office_hours = db.Column(db.String(256))
    




