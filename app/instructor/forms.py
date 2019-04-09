from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import Instructor

class createInstructorForm(FlaskForm):
    name = StringField('InstructorName', validators=[DataRequired()])
    phone = IntegerField('PhoneNumber', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    hours = StringField('OfficeHours')
    submit = SubmitField('Submit')

class deleteInstructorForm(FlaskForm):
    id = IntegerField('Id')
    submit = SubmitField('Submit')

class readInstructorForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired])