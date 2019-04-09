from app.user import bp
from flask import render_template, flash
from flask_login import current_user, login_required
from app.models import User
from app import db
from app.user.forms import DeleteUserForm

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/user.html', user=user)


@bp.route('/index', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('user/index.html', users = users)



@bp.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('/user/create.html')



@bp.route('/read/<username>', methods=['GET', 'POST'])
def read(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/read.html', user=user)


@bp.route('/update/<username>', methods=['GET', 'POST'])
def update(username):
    return render_template('/user/update.html')



@bp.route('/delete/<email>', methods=['GET', 'POST'])
@login_required
def delete(email):
    user = User.query.filter_by(email=email).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted')
    return render_template('/user/delete.html', title='Delete User')
