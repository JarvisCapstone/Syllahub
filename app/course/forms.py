from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class CreateCourseForm(FlaskForm):
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

    # TODO Add Type Validators

class UpdateCourseForm(FlaskForm):
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

class DeleteCourseForm(FlaskForm):
    courseVersion = HiddenField(validators=[DataRequired()])
    courseNumber = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete Course')

    # TODO Add Type Validators
