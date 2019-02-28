from app.home import bp
from flask import render_template
from flask_login import current_user, login_required
from app.models import User

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/user.html', user=user)

@bp.route('/user/index', methods=['GET'])
def userIndex():
    return render_template('home/userindex.html')


