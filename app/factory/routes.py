from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app.factory import bp
from app.factory.forms import GenerateForm, SeedFromWebForm
from app.factory.factory import Factory
from app.auth.routes import admin_required

@bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    gForm = GenerateForm()
    sForm = SeedFromWebForm()
    return render_template('factory/index.html', gForm=gForm, sForm=sForm)


@bp.route('/generate', methods=['POST'])
@admin_required
def generate():
    gForm = GenerateForm()
    if gForm.validate_on_submit():
        flash('Generate Form Validated')
    return redirect(url_for('factory.index'))


@bp.route('/seed', methods=['POST'])
@admin_required
def seed():
    sForm = SeedFromWebForm()
    if sForm.validate_on_submit():
        flash('Seed Form Validated')
    return redirect(url_for('factory.index'))

    

