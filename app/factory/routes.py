from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import User
from app.factory import bp
from app.factory.forms import GenerateForm, SeedFromWebForm, GenerateAdminForm
from app.factory.factory import UserFactory, InstructorFactory, CourseFactory, CloFactory, SyllabusFactory
from app.auth.routes import admin_required

@bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    adminForm = GenerateAdminForm()
    if gForm.generateSubmit.data and gForm.validate():
        print('gForm')
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
    elif sForm.seedSubmit.data and sForm.validate():
        print('sForm')
        flash('Seed Form Validated. TODO')
        # TODO
    elif adminForm.adminSubmit.data and adminForm.validate():
        print('adminForm')
        f = UserFactory()
        message = f.generateAdmin()
        flash(message)
    return render_template('factory/index.html', gForm=gForm, sForm=sForm, adminForm=adminForm)
