from app.course import bp
from flask import render_template, flash
from flask_login import current_user, login_required
from app.models import Course
from app.course.forms import createCourseForm
from app import db

@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('course/index.html')



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



@bp.route('/read/<id>', methods=['GET', 'POST'])
def read(id):
    return render_template('/course/read.html')



@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    return render_template('/course/update.html')



@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    return render_template('/course/delete.html')
