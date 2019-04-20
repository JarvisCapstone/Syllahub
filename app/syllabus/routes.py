import datetime
from app.syllabus import bp
from flask import render_template, flash, jsonify, request, redirect, url_for, make_response
from flask_login import current_user, login_required
from app.models import Syllabus, Course
from app.syllabus.forms import ApproveForm, createSyllabusForm, updateSyllabusForm
from app import db
from sqlalchemy import update
from app.factory.factory import SyllabusFactory

@bp.route('/')
@bp.route('/index')
def index():
    syllabi = Syllabus.query.all()
    return render_template('syllabus/index.html', syllabi=syllabi)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # TODO, add comments
    # do not explicitly call this route
    # syllabi are created in hand with courses
    # and are then updated after that
    form = createSyllabusForm()
    if form.validate_on_submit():
        f = SyllabusFactory()
        data = {}
        data['course_number'] = form.course_number.data, 
        data['course_version'] = form.course_version.data,
        data['section'] = form.section.data, 
        data['semester'] = form.semester.data,
        data['year'] = form.year.data, 
        data['Students_with_disabilities'] = form.SASText.data, 
        data['cheating_policy'] = form.cheatingPolicy.data,
        data['attendance_policy'] = form.attendancePolicy.data, 
        data['grading_policy'] = form.gradingPolicy.data,
        data['required_materials'] = form.requiredMaterials.data, 
        data['optional_materials'] = form.optionalMaterials.data,
        data['meeting_time'] = form.meetingTimes.data, 
        data['withdrawl_date'] = form.withdrawlDate.data

        f.create(data)
        flash("Course Created")

        # TODO redirect on successful create
    elif request.method == 'GET':
        form.cheatingPolicy.data = Syllabus.currentCheatingPolicy
        form.attendancePolicy.data = Syllabus.currentAttendancePolicy
        form.SASText.data = Syllabus.currentSASText
        form.year.data = datetime.date.today().strftime("%Y")
    return render_template('syllabus/create.html', form=form)


@bp.route('/read/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', methods=['GET', 'POST'])
def read(CNumber, CVersion, sec, semester, version, year):
    syllabus = Syllabus.query.filter_by(course_number=CNumber, 
                                        course_version=CVersion, 
                                        section=sec, 
                                        semester=semester, 
                                        version=version, 
                                        year=year).first_or_404()
    '''
    showApproveButton = False
    approveForm = ApproveForm()
    if approveForm.validate_on_submit():
        syllabus.state = 'approved'
        db.session.commit()

    canCurrentUserEdit = False
    if current_user.permission == 'admin':
        canCurrentUserEdit = True
        if syllabus.state == 'draft':
            showApproveButton = True
    i = current_user.instructor
    if i:
        for iSyllabus in i.syllabusList:
            if iSyllabus == syllabus:
                canCurrentUserEdit = True



    if syllabus is not None:
        if showApproveButton:
            return render_template('/syllabus/read.html', 
                                   syllabus=syllabus,
                                   canCurrentUserEdit=canCurrentUserEdit,
                                   showApproveButton=showApproveButton, 
                                   approveForm=approveForm)
        else:
            return render_template('/syllabus/read.html', 
                                   syllabus=syllabus,
                                   canCurrentUserEdit=canCurrentUserEdit,
                                   showApproveButton=showApproveButton)
    
    else:
        flash('Syllabus Not Found')
        return redirect(url_for('syllabus.index'))
    '''
    if syllabus is not None:
        binary_pdf = syllabus.pdf
        response = make_response(binary_pdf)
        response.headers['Content-Type']= 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'course'
        return response

@bp.route('/update/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', methods=['GET', 'POST'])
@login_required
def update(CNumber, CVersion, sec, semester, version, year):
    form = updateSyllabusForm()
    syllabus = Syllabus.query.filter_by(course_number=CNumber, 
                                        course_version=CVersion, 
                                        section=sec, semester=semester, 
                                        version=version, 
                                        year=year).first_or_404()
    if form.validate_on_submit():
        '''
        data = {'course_number':form.course_number.data,
                'course_version':form.course_version.data, 
                'section':form.section.data,
                'version':form.version.data,
                'semester':form.semester.data,
                'year':form.year.data,
                'Students_with_disabilities':form.SASText.data,
                'cheating_policy':form.cheatingPolicy.data,
                'attendance_policy':form.attendancePolicy.data,
                'withdrawl_date':form.withdrawlDate.data, 
                'grading_policy':form.gradingPolicy.data,
                'required_materials':form.requiredMaterials.data,
                'optional_materials':form.optionalMaterials.data,
                'meeting_time':form.meetingTimes.data}
                '''
        syllabus = Syllabus(course_number=form.course_number.data, 
                            course_version=form.course_version.data, 
                            section=form.section.data, semester=form.semester.data,
                            year=form.year.data,Students_with_disabilities=form.SASText.data,
                            cheating_policy=form.cheatingPolicy.data,
                            attendance_policy=form.attendancePolicy.data,
                            withdrawl_date=form.withdrawlDate.data,
                            grading_policy=form.gradingPolicy.data,
                            required_materials=form.optionalMaterials.data,
                            optional_materials=form.optionalMaterials.data)
        
        syllabus.setPDF()
        syllabus.setVersion()
        db.session.add(syllabus)
        db.session.commit()
        flash("Course Updated")

    elif request.method == 'GET':
        form.course_number.data = syllabus.course_number
        form.course_version.data = syllabus.course_version
        form.section.data = syllabus.section
        #form.version.data = syllabus.version
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
@login_required
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
