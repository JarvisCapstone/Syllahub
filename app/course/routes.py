from app.course import bp
from flask import render_template, flash, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from app.auth.routes import admin_required
from app.models import Course
from app.course.forms import CreateCourseForm, UpdateCourseForm, DeleteCourseForm
from app import db
from sqlalchemy import update

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    courses = Course.query.all()
    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # TODO authenticate user
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(number = int(form.courseNumber.data), 
                        version = int(form.courseVersion.data), 
                        name = form.courseName.data, 
                        description = form.courseDescription.data, 
                        prerequisites = form.coursePrereqs.data, 
                        building = form.courseBuilding.data, 
                        room = form.courseRoomNo.data)
      
        course.is_core = form.isCore.data
        course.is_diversity = form.isDiversity.data
        course.is_elr = form.isELR.data
        course.is_wi = form.isWI.data

        db.session.add(course)
        db.session.commit()
        # TODO: Handle case, what if course already exists. crash cleanly
        flash("Course Created!")
    return render_template('course/create.html', title="Create Course", 
                           form=form)

@bp.route('/read/<int:number>/<int:version>', methods=['GET'])
def read(number, version):
    course = Course.query.filter_by(number=number, version=version) \
                         .first_or_404()
    return render_template('/course/read.html', course=course, 
                           number=number, version=version)


@bp.route('/search/<number>/<sortBy>', methods=['GET'])
def search(number, sortBy):
    courses = Course.query.filter_by(number=number).all()
    if (sortBy == 'old'):
        courses.sort(key=lambda x : x.version, reverse=False)
    elif (sortBy == 'new' or form.sortBy == None):
        courses.sort(key=lambda x : x.version, reverse=True)
    return render_template('/course/search.html', courses=courses)


@bp.route('/update/<int:number>/<int:version>', methods=['GET', 'POST'])
@login_required
def update(number, version):
    # TODO authenticate user
    course = Course.query.filter_by(number=number, version=version) \
                         .first_or_404()
    form = UpdateCourseForm()
    deleteForm = DeleteCourseForm(courseNumber=number, courseVersion=version)
    # if this is a validated post request
    if form.validate_on_submit():
        # update course in database
        data = {
            'name':form.courseName.data, 
            'number':form.courseNumber.data, 
            'building':form.courseBuilding.data, 
            'description':form.courseDescription.data,
            'prerequisites':form.coursePrereqs.data, 
            'room':form.courseRoomNo.data,
            'version':form.courseVersion.data, 
            'is_core':form.isCore.data,
            'is_diversity':form.isDiversity.data, 
            'is_elr':form.isELR.data, 
            'is_wi':form.isWI.data
        }
        db.session.query(Course) \
                  .filter_by(number=number, version=version) \
                  .update(data)
        db.session.commit()
        flash("Course Updated")
        # After a successful update, redirect to the read page to show the user
        # the result of their update
        return redirect(url_for('course.read', number=number, version=version))

    elif deleteForm.validate_on_submit():
        #return 'delete validated'
        #course = Course.query.filter_by(number=number, version=version) \
        #                     .first_or_404()
        #db.session.delete(course)
        #db.session.commit()
        # TODO Fix course cascade on delete relationship
        flash('Nick needs to fix cascade on delete for all model '
              'relationships. Please try again later')
        #flash('Course Deleted')
        return redirect(url_for('course.update', number=number, version=version))

    # if this is a get request then the user should recieve a form to use for
    # a future post request
    elif request.method == 'GET':
        form.courseName.data = course.name
        form.courseNumber.data = course.number
        form.courseBuilding.data = course.building
        form.courseDescription.data = course.description
        form.coursePrereqs.data = course.prerequisites
        form.courseRoomNo.data = course.room
        form.courseVersion.data = course.version
        form.isCore.data = course.is_core
        form.isDiversity.data = course.is_diversity
        form.isELR.data = course.is_elr
        form.isWI.data = course.is_wi
        return render_template('/course/update.html', form=form, deleteForm=deleteForm) 
    # if not validated and not a post request, send the standards
    # TODO consider changing this to an error message
    return render_template('/course/update.html', form=form, deleteForm=deleteForm) 


@bp.route('/delete/<int:number>/<int:version>', methods=['GET','POST'])
@login_required
def delete(number,version):
    # TODO authenticate user
    deleteForm = DeleteCourseForm(courseNumber=number, courseVersion=version)
    if deleteForm.validate_on_submit():
        #return 'delete validated'
        #course = Course.query.filter_by(number=number, version=version) \
        #                     .first_or_404()
        #db.session.delete(course)
        #db.session.commit()
        # TODO Fix course cascade on delete relationship
        flash('Nick needs to fix cascade on delete for all model '
              'relationships. Please try again later')
        #flash('Course Deleted')
        return redirect(url_for('course.index'))
    return render_template('/course/delete.html', form=deleteForm)