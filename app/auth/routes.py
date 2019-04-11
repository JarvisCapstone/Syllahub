from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


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
    print("db in register", db)
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = RegistrationForm()
    print("before validate on submit")
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
    return "my_profile"
    #return redirect(url_for('auth.index'))



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