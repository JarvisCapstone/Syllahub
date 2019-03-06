from app.clo import bp
from flask import render_template
from flask_login import current_user, login_required

@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('clo/index.html')



@bp.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('clo/create.html')



@bp.route('/read/<id>', methods=['GET', 'POST'])
def read(id):
    return render_template('/clo/read.html')



@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    return render_template('/clo/update.html')



@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    return render_template('/clo/delete.html')
