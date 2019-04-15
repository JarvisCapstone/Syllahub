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


class DeleteForm(FlaskForm):
    deleteUsersSubmit = SubmitField('Delete all other users')
    deleteInstructorsSubmit = SubmitField('Delete all instructors')
    deleteClosSubmit = SubmitField('Delete all clos')
    deleteCoursesSubmit = SubmitField('Delete all courses')
    deleteSyllabiSubmit = SubmitField('Delete all syllabi')
    deleteAllSubmit = SubmitField('Delete Everything')
