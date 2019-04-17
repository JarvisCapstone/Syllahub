from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class DeleteUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Delete User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Please use a different email address.')

class createUserForm(FlaskForm):
    password = StringField('Password:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    submit = SubmitField('Submit')