from app.clo import bp
from flask import render_template, flash, jsonify, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import Clo
from app.clo.forms import CreateCloForm, UpdateCloForm
from app import db

@bp.route('/index', methods=['GET', 'POST'])
def index():
    clos = Clo.query.all()
    print (clos)
    return render_template('clo/index.html', clos=clos)



@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateCloForm()
    if form.validate_on_submit():
        clo = Clo(general = form.cloGeneral.data, specific = form.cloSpecific.data)
        db.session.add(clo)
        db.session.commit()
        flash("CLOCreated!")
    return render_template('clo/create.html', title="CLO Create", form=form)



@bp.route('/read/<id>', methods=['GET', 'POST'])
def read(id):
    clo = Clo.query.filter_by(id = id).one()
    flash("CLO Read!")
    return render_template('/clo/read.html', title="CLO Read", clo=clo)



@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    clo = Clo.query.filter_by(id = id).one()
    form = UpdateCloForm()
    if form.validate_on_submit():
        if form.cloGeneral.data != '':
            clo.general = form.cloGeneral.data
        if form.cloSpecific.data != '':
            clo.specific = form.cloSpecific.data
        db.session.commit()
        flash("CLO Updated!")
        return redirect(url_for('clo.read', id=id))

    elif request.method == 'GET':
        form.cloGeneral.data = clo.general
        form.cloSpecific.data = clo.specific
        #return render_template('/clo/update.html', title="CLO Update", form=form)

    return render_template('/clo/update.html', title="CLO Update", form=form)



@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    clo = Clo.query.filter_by(id = id).one()
    db.session.delete(clo)
    db.session.commit()
    flash("CLO removed!")
    return redirect(url_for('home.index'))
