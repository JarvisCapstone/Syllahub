from app.instructor import bp
from flask import render_template
from flask_login import current_user, login_required

@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('instructor/index.html')



@bp.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('instructor/create.html')



@bp.route('/read/<id>', methods=['GET', 'POST'])
def read(id):
    return render_template('/instructor/read.html')



@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    return render_template('/instructor/update.html')



@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    return render_template('/instructor/delete.html')
