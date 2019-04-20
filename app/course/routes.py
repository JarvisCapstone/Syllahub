from app.course import bp
from flask import render_template, flash, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from app.auth.routes import admin_required
from app.models import Course, Syllabus
from app.course.forms import CreateCourseForm, UpdateCourseForm, DeleteCourseForm
from app import db
from sqlalchemy import update # TODO, why is this here?

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    courses = Course.query.all()
    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=['GET','POST'])
@login_required
@admin_required
def create():
    # TODO authenticate user
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(number = int(form.courseNumber.data),  
                        name = form.courseName.data, 
                        description = form.courseDescription.data, 
                        prerequisites = form.coursePrereqs.data, 
                        building = form.courseBuilding.data, 
                        room = form.courseRoomNo.data)

        course.setVersion()
        course.is_core = form.isCore.data
        course.is_diversity = form.isDiversity.data
        course.is_elr = form.isELR.data
        course.is_wi = form.isWI.data

        syllabus = Syllabus(course_number = form.courseNumber.data,
                            course_version = course.version,
                            semester = form.semester.data,
                            year = form.semester.data,
                            section = form.section.data)
        syllabus.setVersion()

        db.session.add(syllabus)
        db.session.add(course)
        db.session.commit()
        # TODO: Handle case, what if course already exists. crash cleanly
        flash("Course Created!")
    return render_template('course/create.html', title="Create Course", 
                           form=form)

@bp.route('/read/<number>/<version>', methods=['GET'])
def read(number, version):
    course = Course.query.filter_by(number=number, version=version) \
                         .first_or_404()
    return render_template('/course/read.html', course=course, 
                           number=number, version=version)


@bp.route('/search', methods=['GET'])
def search():
    number = request.args.get('number')
    sortBy = request.args.get('sortBy')
    courses = Course.query.filter_by(number=number).all()
    if (sortBy == 'old'):
        courses.sort(key=lambda x : x.version, reverse=False)
    elif (sortBy == 'new' or form.sortBy == None):
        courses.sort(key=lambda x : x.version, reverse=True)
        
    return render_template('/course/search.html', courses=courses)


@bp.route('/update/<int:number>/<int:version>', methods=['GET', 'POST'])
@login_required
@admin_required
def update(number, version):
    # TODO authenticate user
    oldCourse = Course.query.filter_by(number=number, version=version) \
                         .first_or_404()
    oldSyllabus = Syllabus.query.filter_by(course_number=number, course_version=version) \
                                .first_or_404()
    form = UpdateCourseForm()
    deleteForm = DeleteCourseForm(courseNumber=number, courseVersion=version)
    # if this is a validated post request
    if form.validate_on_submit():
        # update course in database
        course = Course(number = form.courseNumber.data,
                        version = oldCourse.version,  
                        name = form.courseName.data, 
                        description = form.courseDescription.data, 
                        prerequisites = form.coursePrereqs.data, 
                        building = form.courseBuilding.data, 
                        room = form.courseRoomNo.data)

        course.setVersion()
        course.is_core = form.isCore.data
        course.is_diversity = form.isDiversity.data
        course.is_elr = form.isELR.data
        course.is_wi = form.isWI.data

        syllabus = Syllabus(course_number = form.courseNumber.data,
                            course_version = course.version,
                            version = oldSyllabus.version,
                            semester = form.semester.data,
                            year = form.semester.data,
                            section = form.section.data)
        syllabus.setVersion()

        db.session.add(course)
        db.session.add(syllabus)
        db.session.commit()

        flash("Course Updated")
        # After a successful update, redirect to the read page to show the user
        # the result of their update
        return redirect(url_for('course.read', number=number, version=course.version))

    elif deleteForm.validate_on_submit():
        course = Course.query.filter_by(number=number, version=version) \
                             .first_or_404()
        db.session.delete(course)
        db.session.commit()
        flash('Course Deleted')
        return redirect(url_for('course.index'))

    # if this is a get request then the user should recieve a form to use for
    # a future post request
    elif request.method == 'GET':
        form.courseName.data = oldCourse.name
        form.courseNumber.data = oldCourse.number
        form.courseBuilding.data = oldCourse.building
        form.section.data = oldSyllabus.section
        form.year.data = oldSyllabus.year
        form.semester.data = oldSyllabus.semester
        form.courseDescription.data = oldCourse.description
        form.coursePrereqs.data = oldCourse.prerequisites
        form.courseRoomNo.data = oldCourse.room
        form.isCore.data = oldCourse.is_core
        form.isDiversity.data = oldCourse.is_diversity
        form.isELR.data = oldCourse.is_elr
        form.isWI.data = oldCourse.is_wi
        return render_template('/course/update.html', form=form, 
                               deleteForm=deleteForm) 
    # if not validated and not a post request, send the standards
    # TODO consider changing this to an error message
    return render_template('/course/update.html', form=form, 
                           deleteForm=deleteForm) 


@bp.route('/delete/<int:number>/<int:version>', methods=['GET','POST'])
@login_required
def delete(number,version):
    # TODO authenticate user
    deleteForm = DeleteCourseForm(courseNumber=number, courseVersion=version)
    if deleteForm.validate_on_submit():
        course = Course.query.filter_by(number=number, version=version) \
                             .first_or_404()
        db.session.delete(course)
        db.session.commit()
        flash('Course Deleted')
        return redirect(url_for('course.index'))
    return render_template('/course/delete.html', form=deleteForm)