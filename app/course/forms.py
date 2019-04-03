from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Course

class createCourseForm(FlaskForm):
    courseName = StringField('Course Name', validators=[DataRequired()])
    courseNumber = StringField('Course Number', validators=[DataRequired()])
    courseVersion = StringField('Course Version', validators=[DataRequired()])
    courseDescription = StringField('Course Description')
    coursePrereqs = StringField('Course Prereques')
    courseBuilding = StringField('Building')
    courseRoomNo = StringField('Room Number')
    isCore = BooleanField('Satisfies core requirement?')
    isWI = BooleanField('Satisfies writing intensive requirement?')
    isELR = BooleanField('Satisfies experimental learning requirement?')
    isDiversity = BooleanField('Satisfies diversity requirement?')