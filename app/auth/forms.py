from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
        EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class assignInstructorToCourse(FlaskForm):
    courseNumber = StringField('Course Number', validators=[DataRequired()])
    courseSection = StringField('Course Section', validators=[DataRequired()])
    semester = SelectField('Semester', choices=[('spring','Spring'), ('fall','Fall'), ('summer','Summer')])
    year = StringField('Year', validators=[DataRequired()])
    syllabusVersion = StringField('Syllabus Version', validators=[DataRequired()])
    courseVersion = StringField('Course Version', validators=[DataRequired()])
    instructorID = StringField('Instructor ID', validators=[DataRequired()])

class RequestReloginForm(FlaskForm):
    logout = SubmitField('Logout')
