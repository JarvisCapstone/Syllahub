from functools import wraps
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.auth import bp

from app.auth.forms import LoginForm, RegistrationForm, assignInstructorToCourse, RequestReloginForm, assignCloToCourse
from app.syllabus.forms import ApproveForm
from app.models import User, SyllabusInstructorAssociation, Syllabus, Instructor, course_clo_table, Course


def redirect_url(default='home.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')

        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        instructor = Instructor(email=form.email.data)
        db.session.add(instructor)
        db.session.commit()
        newinstructor = Instructor.query.filter_by(email = form.email.data).first()
        user = User(email=form.email.data, instructor_id = newinstructor.id)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user! Please provide some additional iformation')
        return redirect(url_for('instructor.update', id=newinstructor.id))
    return render_template('auth/register.html', title='Register',
                           form=form)


@bp.route('/my_profile')
@login_required
def my_profile():
    if current_user.permission == 'admin':
        approveForm = ApproveForm()
        if approveForm.validate_on_submit():
            syllabus.state = 'approved'
            db.session.commit()
        draftSyllabi = Syllabus.query.filter_by(state='draft').all()
        return render_template('auth/admin_profile.html', 
                               current_user=current_user,
                               draftSyllabi=draftSyllabi,
                               approveForm=approveForm)
    else:
        return render_template('auth/instructor_profile.html')
    #return redirect(url_for('auth.index'))

@bp.route('/assignInstruct', methods=['GET', 'POST'])
@login_required
def assignInstruct():
    form = assignInstructorToCourse()
    if form.validate_on_submit():
        relationship = SyllabusInstructorAssociation(
                           syllabus_course_number = int(form.courseNumber.data), 
                           syllabus_course_version = int(form.courseVersion.data), 
                           syllabus_semester = form.semester.data, 
                           syllabus_year = form.year.data, 
                           syllabus_version = form.syllabusVersion.data, 
                           instructor_id = form.instructorID.data,
                           syllabus_section = form.courseSection.data)
        db.session.add(relationship)
        db.session.commit()
        flash("Assignment Made!")
        return redirect(url_for('auth.my_profile'))
    return render_template('auth/assignInstruct.html', form=form)

@bp.route('/assignClo', methods=['GET', 'POST'])
@login_required
def assignClo():
    form = assignCloToCourse()
    if form.validate_on_submit():
        # relationship = course_clo_table(course_number = int(form.courseNumber.data),
        #                                 course_version = int(form.courseVersion.data),
        #                                 clo_id = int(form.cloID.data))

        # TODO. this is completly unneeded. delete this and use the models.
        # TODO. course.clos.append(clo)
        db.session.execute("INSERT INTO course_clo VALUES ("+ (form.courseNumber.data) +
                         ", " + (form.courseVersion.data) + ", " + (form.cloID.data) + ");")
        #db.session.add(relationship)
        db.session.commit()
        flash("Created relationship between CLO and Course!")
        return redirect(url_for('auth.my_profile'))
    return render_template('auth/assignClo.html', form=form)


@bp.route('/myCourses', methods=['GET', 'POST'])
@login_required
def myCourses():
    #print (current_user.email)
    # who wrote this? you can do all of this in one line of code
    # courses = current_user.courses <--- thats it. delete the rest of this
    user = User.query.filter_by(email=current_user.email).first()
    associations = SyllabusInstructorAssociation.query.filter_by(instructor_id=user.instructor_id).all()
    courseNumsAndVersions = list()
    courses = list()
    for association in associations:
        courseNumsAndVersions.append((association.syllabus_course_number,
                                    association.syllabus_course_version,
                                    association.syllabus_section,
                                    association.syllabus_semester,
                                    association.syllabus_year,
                                    association.syllabus_version))
    for info in courseNumsAndVersions:
        courses.append( ( Course.query.filter_by(number=info[0], version=info[1]).first(),
                        Syllabus.query.filter_by(course_number=info[0], course_version=info[1],
                                                section=info[2], semester=info[3], year=info[4]).first() ) )
    return render_template('auth/my_courses.html', courses=courses)

@bp.route('/requestRelogin', methods=['GET','POST'])
@login_required
def requestRelogin():
    next=request.args.get('next')
    form = RequestReloginForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('auth.login', next=next))
    return render_template('auth/requestRelogin.html', form=form)


def admin_required(func):
    '''Restricts access to routes if the user is not logged in with admin privlages
    If you decorate a view with this, it will ensure that the current user is
    logged in and has a permission = 'admin'
    
    Example useage:
        @app.route('/post')
        @admin_required
        def post():
            pass

    import with:
        from app.auth.routes import admin_required

    '''
    @wraps(func)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.permission != 'admin':
            flash("This page requires administrator privlages to access")
            return redirect(url_for('auth.requestRelogin', 
                            next=url_for(request.endpoint)))
        return func(*args, **kwargs)
    return decorated_function