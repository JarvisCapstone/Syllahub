from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, assignInstructorToCourse
from app.models import User, SyllabusInstructorAssociation, Syllabus


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        print("validated")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home.index'))
    return render_template('auth/register.html', title='Register',
                           form=form)


@bp.route('/my_profile')
@login_required
def my_profile():
    if current_user.permission == 'admin':
        draftSyllabi = Syllabus.query.filter_by(state='draft').all()
        return render_template('auth/admin_profile.html',draftSyllabi=draftSyllabi)
    else:
        return render_template('auth/instructor_profile.html')
    #return redirect(url_for('auth.index'))

@bp.route('/assignInstruct', methods=['GET', 'POST'])
@login_required
def assignInstruct():
    form = assignInstructorToCourse()
    if form.validate_on_submit():
        relationship = SyllabusInstructorAssociation(syllabus_course_number = int(form.courseNumber.data), 
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



def admin_required(func):
    '''Decorator used to see if current user has administrator status
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.permission != 'admin':
            flash("This action requires administrator privlages")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return decorated_function