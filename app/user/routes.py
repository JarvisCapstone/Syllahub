from app.user import bp
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app import db
from app.user.forms import DeleteUserForm, createUserForm

@bp.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template('user/user.html', user=user)


@bp.route('/index', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)



@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = createUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password = form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.read', id=user.id))
    return render_template('/user/create.html', title="Create User", form=form)



@bp.route('/read/<email>', methods=['GET', 'POST'])
def read(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template('user/read.html', user=user)


@bp.route('/update/<email>', methods=['GET', 'POST'])
def update(email):
    return render_template('/user/update.html')



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