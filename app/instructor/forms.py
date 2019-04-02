from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import Instructor

class createInstructorForm(FlaskForm):
    name = StringField('InstructorName')
    phone = IntegerField('PhoneNumber')
    email = StringField('Email')
    hours = StringField('OfficeHours')
    submit = SubmitField('Submit')