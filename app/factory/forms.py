from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class GenerateForm(FlaskForm):
    count = IntegerField('How many fake users do you want?')
    submit = SubmitField('Generate')


class SeedFromWebForm(FlaskForm):
    #courseVersion = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Get Data')
