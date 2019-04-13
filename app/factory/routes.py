from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app.factory import bp
from app.factory.forms import GenerateForm, SeedFromWebForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #TODO. make this auth required
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    return render_template('factory/index.html', gForm=gForm, sForm=sForm)


@bp.route('/generate', methods=['POST'])
@login_required
def generate():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    if gForm.validate_on_submit():
        flash('validated g form')
    return render_template('factory/index.html', gForm=gForm, sForm=sForm)


@bp.route('/seed', methods=['POST'])
@login_required
def seed():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    if sForm.validate_on_submit():
        flash('validated s form')
    return render_template('factory/index.html', gForm=gForm, sForm=sForm)

    

