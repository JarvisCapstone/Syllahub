from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class GenerateForm(FlaskForm):
    count = IntegerField('How many fake things do you want?')
    generateSubmit = SubmitField('Generate')


class SeedFromWebForm(FlaskForm):
    #courseVersion = HiddenField(validators=[DataRequired()])
    seedSubmit = SubmitField('Get Data')


class GenerateAdminForm(FlaskForm):
    adminSubmit = SubmitField('Create Admin')