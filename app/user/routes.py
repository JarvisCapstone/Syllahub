from app.user import bp
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app import db
from app.user.forms import DeleteUserForm, createUserForm, updateUserForm

@bp.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template('user/user.html', user=user)


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)



@bp.route('/create', methods=['GET', 'POST'])
def create():

    return redirect(url_for('auth.register'))



@bp.route('/read/<email>', methods=['GET', 'POST'])
def read(email):
    user = User.query.filter_by(email=email).first()
    return render_template('user/read.html', user=user)


@bp.route('/update/', methods=['GET', 'POST'])
@login_required
def update():
    currentUser = current_user
    form = updateUserForm()
    if form.validate_on_submit():
        if currentUser.check_password(form.currentPassword.data):
            currentUser.set_password(form.newPassword.data)
            db.session.add(currentUser)
            db.session.commit()
            flash("Password Updated!")
        else:
            flash('Invalid Password')
    return render_template('/user/update.html', form=form)

    

@bp.route('/delete/<email>', methods=['GET', 'POST'])
@login_required
def delete(email):
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        flash("Succesfully Deleted User")
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('/user/delete.html', form=form)