from app.course import bp
from flask import render_template, flash, jsonify
from flask_login import current_user, login_required
from app.models import Course
from app.course.forms import createCourseForm, updateCourseForm
from app import db
from sqlalchemy import update

@bp.route('/index', methods=['GET'])
def index():
    courses = Course.query.all()
    print (courses)
    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = createCourseForm()
    if form.validate_on_submit():
        course = Course(number = int(form.courseNumber.data), version = int(form.courseVersion.data), 
                        name = form.courseName.data, description = form.courseDescription.data, 
                        prerequisites = form.coursePrereqs.data, building = form.courseBuilding.data, 
                        room = form.courseRoomNo.data)
      
        course.is_core = form.isCore.data
        course.is_diversity = form.isDiversity.data
        course.is_elr = form.isELR.data
        course.is_wi = form.isWI.data

        db.session.add(course)
        db.session.commit()
        flash("Course Created!")
    return render_template('course/create.html', title="Create Course", form=form)

@bp.route('/read/<number>/<version>', methods=['GET'])
def read(number, version):
    course = Course.query.filter_by(number=number, version=version).first()
    return render_template('/course/read.html', course=course, number=number, version=version)

@bp.route('/search/<number>/<sortBy>', methods=['GET'])
def search(number, sortBy):
    courses = Course.query.filter_by(number=number).all()
    if (sortBy == 'old'):
        courses.sort(key=lambda x : x.version, reverse=False)
    elif (sortBy == 'new' or form.sortBy == None):
        courses.sort(key=lambda x : x.version, reverse=True)
    return render_template('/course/search.html', courses=courses)

@bp.route('/update/<number>/<version>', methods=['GET', 'POST'])
def update(number, version):
    course = Course.query.filter_by(number=number, version=version).first()
    form = updateCourseForm()
    if course is not None:
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
        if form.validate_on_submit():
            data = {'name':form.courseName.data, 'number':form.courseNumber.data, 
                    'building':form.courseBuilding.data, 'description':form.courseDescription.data,
                    'prerequisites':form.coursePrereqs.data, 'room':form.courseRoomNo.data,
                    'version':form.courseVersion.data, 'is_core':form.isCore.data,
                    'is_diversity':form.isDiversity.data, 'is_elr':form.isELR.data, 'is_wi':form.isWI.data}
            db.session.query(Course).filter_by(number=number, version=version).update(data)
            db.session.commit()
            flash("Course Updated")
    return render_template('/course/update.html', form=form)

@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    return render_template('/course/delete.html')
