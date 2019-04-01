from app.home import bp
from flask import render_template
from flask_login import current_user, login_required
from app.models import User
#from app.models import *

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@bp.route('/olduser/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/user.html', user=user)

@bp.route('/olduserindex', methods=['GET', 'POST'])
def userIndex():
    users = User.query.all()
    return render_template('home/userindex.html', users = users)

@bp.route('/site_map', methods=['GET', 'POST'])
def site_map():
    print("3333333333333333333333333 site map called ")
    return render_template('home/site_map.html')

@bp.route('/run', methods=['GET', 'POST'])
def run():
    print('run called')
    return 'success'
