from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import Instructor

class createInstructorForm(FlaskForm):
    name = StringField('Instructor Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    hours = StringField('Office Hours')
    submit = SubmitField('Submit')

class deleteInstructorForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    submit = SubmitField('Submit')

class updateInstructorForm(FlaskForm):
    id = IntegerField('Id,', validators=[DataRequired()])
    name = StringField('Instructor')
    phone = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired()])
    hours = StringField('Office Hours')  