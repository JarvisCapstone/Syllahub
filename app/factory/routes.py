from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app.factory import bp
from app.factory.forms import GenerateForm, SeedFromWebForm
from app.factory.factory import UserFactory, InstructorFactory, CourseFactory, CloFactory, SyllabusFactory
from app.auth.routes import admin_required

@bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    return render_template('factory/index.html', gForm=gForm, sForm=sForm)


@bp.route('/generate', methods=['POST'])
@admin_required
def generate():
    gForm = GenerateForm()
    if gForm.validate_on_submit():
        count = int(gForm.count.data)
        factories = []
        factories.append(UserFactory())
        factories.append(InstructorFactory())
        factories.append(CourseFactory())
        factories.append(CloFactory())
        factories.append(SyllabusFactory())
        print(factories)
        for factory in factories:
            factory.addToDB(count)
        message= "added {} fake data entries to each table in db".format(count)
        flash(message)
    return redirect(url_for('factory.index'))


@bp.route('/seed', methods=['POST'])
@admin_required
def seed():
    sForm = SeedFromWebForm()
    if sForm.validate_on_submit():
        flash('Seed Form Validated')
        # TODO
    return redirect(url_for('factory.index'))

