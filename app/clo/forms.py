from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Clo


class CreateCloForm(FlaskForm):
    cloGeneral = StringField('general', validators=[DataRequired()])
    cloSpecific = StringField('specific', validators=[DataRequired()])

class DeleteCloForm(FlaskForm):
    cloID = StringField('ID', validators=[DataRequired()])

class ReadCloForm(FlaskForm):
    cloID = StringField('ID', validators=[DataRequired()])

class UpdateCloForm(FlaskForm):
    cloID = StringField('ID', validators=[DataRequired()])
    cloGeneral = StringField('general')
    cloSpecific = StringField('specific')