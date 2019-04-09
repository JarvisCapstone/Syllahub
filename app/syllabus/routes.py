import datetime
from app.syllabus import bp
from flask import render_template, flash, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Syllabus, Course
from app.syllabus.forms import createSyllabusForm, updateSyllabusForm
from app import db
from sqlalchemy import update

@bp.route('/index', methods=['GET'])
def index():
    syllabi = Syllabus.query.all()
    return render_template('syllabus/index.html', syllabi=syllabi)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = createSyllabusForm()
    if form.validate_on_submit():
        syllabus = Syllabus(course_number=form.course_number.data, course_version=form.course_version.data,
                                section=form.section.data, version=form.version.data, semester=form.semester.data,
                                year=form.year.data, Students_with_disabilities=form.SASText.data, cheating_policy=form.cheatingPolicy.data,
                                attendance_policy=form.attendancePolicy.data, grading_policy=form.gradingPolicy.data,
                                required_materials=form.requiredMaterials.data, optional_materials=form.optionalMaterials.data,
                                meeting_time=form.meetingTimes.data, withdrawl_date=form.withdrawlDate.data)
        if syllabus is not None:
            db.session.add(syllabus)
            db.session.commit()
            flash("Syllabus Created!")
        else:
            flash("That course does not exist")
    elif request.method == 'GET':
        form.cheatingPolicy.data = "University policy 3-01.8 deals with the problem of academic dishonesty, cheating, and plagiarism.  None of these will be tolerated in this class.  The sanctions provided in this policy will be used to deal with any violations.  If you have any questions, please read the policy at http://www.kent.edu/policyreg/administrative-policy-regarding-student-cheating-and-plagiarism and/or ask."
        form.attendancePolicy.data = "Purpose. Regular attendance in class is expected of all students at all levels at the university. While classes are conducted on the premise that regular attendance is expected, the university recognizes certain activities, events, and circumstances as legitimate reasons for absence from class. This policy provides for accommodations in accordance with federal and state laws prohibiting discrimination, including, but not limited to, Section 504 of the Rehabilitation Act of 1973, 29 U.S.C.§794, and its implementing regulation, 34 C.F.R. Part 104; Title II of the Americans with Disabilities Act of 1990, 42 U.S.C. §12131 et seq., and its implementing regulations, 28 C.F.R. Part 35; as well as university policy 5-16. More information can be found at https://www.kent.edu/policyreg/administrative-policy-regarding-class-attendance-and-class-absence"
        form.SASText.data = "University policy 3-01.3 requires that students with disabilities be provided reasonable accommodations to ensure their equal access to course content.  If you have a documented disability and require accommodations, please contact the instructor at the beginning of the semester to make arrangements for necessary classroom adjustments.  Please note, you must 	first verify your eligibility for these through Student Accessibility Services (contact 330-672-3391 or visit www.kent.edu/sas for more information on registration procedures)."
        form.year.data = datetime.date.today().strftime("%Y")
    return render_template('syllabus/create.html', form=form)

@bp.route('/read/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', methods=['GET', 'POST'])
def read(CNumber, CVersion, sec, semester, version, year):
    syllabus = Syllabus.query.filter_by(course_number=CNumber, course_version=CVersion, 
                                        section=sec, semester=semester, version=version, 
                                        year=year).first()
    if syllabus is not None:
        return render_template('/syllabus/read.html', syllabus=syllabus)
    else:
        flash('Syllabus Not Found')
        return redirect(url_for('home.index'))

@bp.route('/update/<CNumber>/<CVersion>/<sec>/<semester>/<version>/<year>', methods=['GET', 'POST'])
def update(CNumber, CVersion, sec, semester, version, year):
    form = updateSyllabusForm()
    syllabus = Syllabus.query.filter_by(course_number=CNumber, course_version=CVersion, 
                                        section=sec, semester=semester, version=version, 
                                        year=year).first()
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
                                        year=year).first()
    if syllabus is not None:
        db.session.delete(syllabus)
        db.session.commit()
        flash("Deleted Syllabus")
        return redirect(url_for('home.index'))
    return redirect(url_for('home.index'))
