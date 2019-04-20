from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Course

class createSyllabusForm(FlaskForm):
    course_number = StringField('Course Number',validators=[DataRequired()])
    course_version = StringField('Course Version',validators=[DataRequired()])
    section = StringField('Section',validators=[DataRequired()])
    semester = SelectField(choices=[('spring','Spring'), ('fall','Fall'), ('summer','Summer')])
    year = StringField('Year', validators=[DataRequired()])
    SASText = TextAreaField('Student Accesability Info', validators=[DataRequired()])
    cheatingPolicy = TextAreaField('Cheating Policy', validators=[DataRequired()])
    attendancePolicy = TextAreaField('Attendance Policy', validators=[DataRequired()])
    withdrawlDate = StringField('WithdrawlDate', validators=[DataRequired()])
    gradingPolicy = TextAreaField('Grading Policy', validators=[DataRequired()])
    requiredMaterials = StringField('Required Materials')
    optionalMaterials = StringField('Optional Materials')
    meetingTimes = StringField('Meeting Times', validators=[DataRequired()])

class updateSyllabusForm(FlaskForm):
    course_number = StringField('Course Number',validators=[DataRequired()])
    course_version = StringField('Course Version',validators=[DataRequired()])
    section = StringField('Section',validators=[DataRequired()])
    #version = StringField('Syllabus Version',validators=[DataRequired()])
    semester = SelectField(choices=[('spring','Spring'), ('fall','Fall'), ('summer','Summer')])
    year = StringField('Year', validators=[DataRequired()])
    SASText = TextAreaField('Student Accesability Info', validators=[DataRequired()])
    cheatingPolicy = TextAreaField('Cheating Policy', validators=[DataRequired()])
    attendancePolicy = TextAreaField('Attendance Policy', validators=[DataRequired()])
    withdrawlDate = StringField('WithdrawlDate', validators=[DataRequired()])
    gradingPolicy = TextAreaField('Grading Policy', validators=[DataRequired()])
    requiredMaterials = StringField('Required Materials')
    optionalMaterials = StringField('Optional Materials')
    meetingTimes = StringField('Meeting Times', validators=[DataRequired()])
    
class ApproveForm(FlaskForm):
    approveSubmit = SubmitField('Approve')


