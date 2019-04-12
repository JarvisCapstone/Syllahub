import datetime
from app.syllabus import bp
from flask import render_template, flash, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Syllabus, Course
from app.syllabus.forms import createSyllabusForm, updateSyllabusForm
from app import db
from sqlalchemy import update

@bp.route('/')
@bp.route('/index')
def index():
    syllabi = Syllabus.query.all()
    return render_template('syllabus/index.html', syllabi=syllabi)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # TODO, add comments
    form = createSyllabusForm()
    if form.validate_on_submit():
        syllabus = Syllabus(course_number=form.course_number.data, 
                            course_version=form.course_version.data,
                            section=form.section.data, 
                            version=form.version.data, 
                            semester=form.semester.data,
                            year=form.year.data, 
                            Students_with_disabilities=form.SASText.data, 
                            cheating_policy=form.cheatingPolicy.data,
                            attendance_policy=form.attendancePolicy.data, 
                            grading_policy=form.gradingPolicy.data,
                            required_materials=form.requiredMaterials.data, 
                            optional_materials=form.optionalMaterials.data,
                            meeting_time=form.meetingTimes.data, 
                            withdrawl_date=form.withdrawlDate.data)
        if syllabus is not None:
            db.session.add(syllabus)
            db.session.commit()
            flash("Syllabus Created!")
        else:
            flash("That course does not exist")
        # TODO redirect on successful create
    elif request.method == 'GET':
        form.cheatingPolicy.data = Syllabus.currentCheatingPolicy
        form.attendancePolicy.data = Syllabus.currentAttendancePolicy
        form.SASText.data = Syllabus.currentSASText
        form.year.data = datetime.date.today().strftime("%Y")
    return render_template('syllabus/create.html', form=form)

@bp.route('/read/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', 
          methods=['GET', 'POST'])
def read(CNumber, CVersion, sec, semester, version, year):
    syllabus = Syllabus.query.filter_by(course_number=CNumber, 
                                        course_version=CVersion, 
                                        section=sec, semester=semester, 
                                        version=version, 
                                        year=year).first_or_404()
    if syllabus is not None:
        return render_template('/syllabus/read.html', syllabus=syllabus)
    else:
        flash('Syllabus Not Found')
        return redirect(url_for('home.index'))

@bp.route('/update/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', 
          methods=['GET', 'POST'])
def update(CNumber, CVersion, sec, semester, version, year):
    form = updateSyllabusForm()
    syllabus = Syllabus.query.filter_by(course_number=CNumber, 
                                        course_version=CVersion, 
                                        section=sec, semester=semester, 
                                        version=version, 
                                        year=year).first_or_404()
    if form.validate_on_submit():
        data = {'course_number':form.course_number.data, 'course_version':form.course_version.data, 
                'section':form.section.data, 'version':form.version.data,
                'semester':form.semester.data, 'year':form.year.data,
                'Students_with_disabilities':form.SASText.data, 'cheating_policy':form.cheatingPolicy.data,
                'attendance_policy':form.attendancePolicy.data, 'withdrawl_date':form.withdrawlDate.data, 
                'grading_policy':form.gradingPolicy.data, 'required_materials':form.requiredMaterials.data,
                'optional_materials':form.optionalMaterials.data, 'meeting_time':form.meetingTimes.data}
        db.session.query(Syllabus).filter_by(course_number=CNumber, course_version=CVersion, 
                                        section=sec, semester=semester, version=version, 
                                        year=year).update(data)
        db.session.commit()
        flash("Course Updated")
    elif request.method == 'GET':
        form.course_number.data = syllabus.course_number
        form.course_version.data = syllabus.course_version
        form.section.data = syllabus.section
        form.version.data = syllabus.version
        form.semester.data = syllabus.semester
        form.year.data = syllabus.year
        form.SASText.data = syllabus.Students_with_disabilities
        form.cheatingPolicy.data = syllabus.cheating_policy
        form.attendancePolicy.data = syllabus.attendance_policy
        form.withdrawlDate.data = syllabus.withdrawl_date
        form.withdrawlDate.data = syllabus.withdrawl_date
        form.gradingPolicy.data = syllabus.grading_policy
        form.requiredMaterials.data = syllabus.required_materials
        form.optionalMaterials.data = syllabus.optional_materials
    return render_template('/syllabus/update.html', form=form)

@bp.route('/delete/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', methods=['GET', 'POST'])
def delete(CNumber, CVersion, sec, semester, version, year):
    syllabus = Syllabus.query.filter_by(course_number=CNumber, course_version=CVersion, 
                                        section=sec, semester=semester, version=version, 
                                        year=year).first_or_404()
    if syllabus is not None:
        db.session.delete(syllabus)
        db.session.commit()
        flash("Deleted Syllabus")
        return redirect(url_for('home.index'))
    return redirect(url_for('home.index'))
