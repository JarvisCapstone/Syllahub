from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#from app.models import Clo


class CreateCloForm(FlaskForm):
    cloGeneral = StringField('general', validators=[DataRequired()])
    cloSpecific = StringField('specific', validators=[DataRequired()])

class UpdateCloForm(FlaskForm):
    cloGeneral = StringField('general')
    cloSpecific = StringField('specific')

class DeleteCloForm(FlaskForm):
    cloID = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete CLO')
    