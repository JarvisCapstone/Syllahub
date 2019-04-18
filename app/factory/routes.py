from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import User
from app.factory import bp
from app.factory.forms import DeleteForm, GenerateForm, SeedFromWebForm, GenerateAdminForm
from app.factory.factory import UserFactory, InstructorFactory, CourseFactory, CloFactory, SyllabusFactory
from app.factory.webparse import Retriever
from app.auth.routes import admin_required

@bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    adminForm = GenerateAdminForm()
    deleteForm = DeleteForm()
    if gForm.generateSubmit.data and gForm.validate():
        count = int(gForm.count.data)
        factories = []
        factories.append(UserFactory())
        factories.append(InstructorFactory())
        factories.append(CourseFactory())
        factories.append(CloFactory())
        factories.append(SyllabusFactory())
        for factory in factories:
            factory.createFakes(count)
        message= "added {} fake data entries to each table in db".format(count)
        flash(message)

    elif sForm.seedSubmit.data and sForm.validate():
        flash('Seed Form Validated. TODO')
        r = Retriever()
        r.run()
        # TODO

    elif adminForm.adminSubmit.data and adminForm.validate():
        f = UserFactory()
        message = f.createAdmin()
        flash(message)
    
    elif deleteForm.deleteUsersSubmit.data and deleteForm.validate():
        UserFactory.deleteAll()

    elif deleteForm.deleteInstructorsSubmit.data and deleteForm.validate():
        InstructorFactory.deleteAll()

    elif deleteForm.deleteCoursesSubmit.data and deleteForm.validate():
        CourseFactory.deleteAll()

    elif deleteForm.deleteClosSubmit.data and deleteForm.validate():
        CloFactory.deleteAll()

    elif deleteForm.deleteSyllabiSubmit.data and deleteForm.validate():
        SyllabusFactory.deleteAll()

    elif deleteForm.deleteAllSubmit.data and deleteForm.validate():
        UserFactory.deleteAll()
        InstructorFactory.deleteAll()
        CourseFactory.deleteAll()
        CloFactory.deleteAll()
        SyllabusFactory.deleteAll()
        

    return render_template('factory/index.html', gForm=gForm, sForm=sForm, 
                           adminForm=adminForm, deleteForm=deleteForm)
