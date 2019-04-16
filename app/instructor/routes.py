from app.instructor import bp
from app.models import Instructor, User
from flask import render_template, jsonify, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.instructor.forms import createInstructorForm, deleteInstructorForm, updateInstructorForm


@bp.route('/index', methods=['GET', 'POST'])
def index():
    instructors = Instructor.query.all()
    print(instructors)

    return render_template('instructor/index.html', instructors=instructors)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = createInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor(name=form.name.data, phone=form.phone.data, 
                                email=form.email.data, perfered_office_hours=form.hours.data)
        db.session.add(instructor)
        db.session.commit()
        return redirect(url_for('instructor.read', id=instructor.id))
    return render_template('instructor/create.html', title="Create Instructor", form=form)


@bp.route('/read/<id>', methods=['GET'])
def read(id):
    instructor = Instructor.query.filter_by(id=id).first()
    return render_template('/instructor/read.html', instructor=instructor)


@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    form = updateInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor.query.filter_by(id = int(form.id.data)).one()
        instructor.id = form.id.data
        instructor.name = form.name.data
        instructor.phone = form.phone.data
        instructor.email = form.email.data
        instructor.hours = form.hours.data

        db.session.commit()
        
        flash("Instructor Updated!")
        return redirect(url_for('instructor.read', id=instructor.id))

    return render_template('/instructor/update.html', form=form)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    form = deleteInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor.query.filter_by(id=form.id.data).first_or_404()
        flash("Succesfully Deleted Instructor")
        db.session.delete(instructor)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('/instructor/delete.html', form=form)

     