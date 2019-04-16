from fpdf import FPDF
from app import db
from app.models import Syllabus, SyllabusInstructorAssociation, Course, Instructor, Clo
from sqlalchemy_utils import Timestamp
from sqlalchemy import and_, Boolean, Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, MetaData, String, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import update

class syllabusGenerator():
    
    def pdf_Generate(course_number=33211, course_version=1,
                     section=1, semester='summer', version=0, year=2019):

        #Pull Syllabus information
        syllabus = Syllabus.query.filter_by(course_number=course_number,
                                            course_version=course_version,
                                            section=section, semester=semester,
                                            version=version,
                                            year=year).first_or_404()

        #Pull Relationship between syllabus and instructor
        syllabusInstructor = SyllabusInstructorAssociation.query.filter_by(
            syllabus_course_number=course_number,
            syllabus_course_version=course_version,
            syllabus_section = section, syllabus_semester = semester,
            syllabus_version= version, syllabus_year=year
        ).first_or_404()

        #Use Relationship to pull instructor information
        instructor = Instructor.query.filter_by(id=syllabusInstructor.instructor_id) \
        .first_or_404()

        #Pull Course Information from the given Syllabus Course Number and version
        course = Course.query.filter_by(number = course_number,
                                        version = course_version) \
                                            .first_or_404()

        


        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'CS' + str(course_number), ln=1, align='C')
        pdf.cell(0, 10, 'Course Syllabus', ln=1, align='C')
        pdf.ln(5)

        pdf.set_font_size(10)

        #TODO, once we find out relationships
        pdf.cell(0, 10, instructor.name, ln=1, align='C')
        pdf.ln(5)
        pdf.cell(0, 10, semester + ' ' + str(year) + ' Semester', ln=1, align='C')
        #TODO, make section number a string in database, add check
        # for section to determine campus
        pdf.cell(0, 10, 'Kent Campus, Section: ' + str(section), ln=1, align='C')
        pdf.ln(5)
        #TODO, fix once room number and building are moved to syllabus
        #TODO, revamp meeting_time once we get delimiter solved
        if (syllabus.meeting_time != None):
            pdf.cell(0, 10, 'Meetings Times: '+ syllabus.meeting_time + ', ' +
            str(course.room) + ' ' + course.building , ln=1, align='C')
        else:
            pdf.cell(0, 10, 'This is an online course, there is no meeting times',
                    ln=1, align='C')
        pdf.ln(10)

        #TODO, optional, once in db
        #if introduction != null:
        pdf.cell(0,10, 'Instructor Introduction', ln=1)
        pdf.cell(0,10, 'Walker is a very nice man who is teaching this course',
                ln=1)

        pdf.cell(0,10, 'Contact Information', ln=1)
        #TODO, once we find out relations
        pdf.cell(0,10, 'Email: ' + instructor.email, ln=1)
        pdf.cell(0,10, 'Phone: ' + str(instructor.phone), ln=1)
        #TODO, include office room in database
        pdf.cell(0,10, 'Office: #####', ln=1)
        pdf.cell(0,10, 'Office Hours: ' + instructor.perfered_office_hours, ln=1)
        pdf.ln(5)

        pdf.cell(0,10, 'Course Description from the University Catalog', ln=1)
        pdf.cell(0,10, 'CS'+str(course_number) + ' ' + course.name + ': ' +
                course.description, ln=1)    
        if (course.prerequisites != None):
            pdf.cell(0,10, 'Prerequisite: ' + course.prerequisites, ln=1)
        pdf.ln(5)

        pdf.cell(0,10, 'Course Learning Outcomes', ln=1)
        pdf.cell(0,10, 'By the end of this course, you should be able to:', ln=1)
        #TODO, for each clo in course
        # pdf.cell(0,10, clo.general, ln=1)

        #TODO, required should be moved to course, no syllabus
        #if (course.required_materials != None)
            #pdf.cell(0,10, 'Required Materials, ln=1)
            #pdf.cell(0,10, course.required_materials, ln=1)
        if (syllabus.optional_materials != None):
            pdf.cell(0,10, 'Optional Materials', ln=1)
            pdf.cell(0,10, syllabus.optional_materials, ln=1)

        #TODO, enforce notnull dates / policies      
        
        pdf.cell(0,10, 'Grading Policy', ln=1)
        #pdf.cell(0,10, syllabus.grading_policy, ln=1)
  
        pdf.cell(0,10, 'Registration Date', ln=1)
        pdf.cell(0,10, 'https://www.kent.edu/registrar/fall-your-time-register', ln=1)

        pdf.cell(0,10, 'Withdrawl Date', ln=1)
        pdf.cell(0,10, 'https://www.kent.edu/registrar/spring-important-dates', ln=1)

        pdf.cell(0,10, 'Attendance Policy', ln=1)
        pdf.cell(0,10, 'Attendance Policy goes here', ln=1)

        pdf.cell(0,10, 'Student Accessability Services', ln=1)
        pdf.cell(0,10, 'Important info here', ln=1)

        pdf.cell(0,10, 'Academic Integrity', ln=1)
        pdf.cell(0,10, "Don't plagarize bad", ln=1)

        if (syllabus.extra_policies != None):
            pdf.cell(0,10, 'Extra Policies', ln=1)
            pdf.cell(0,10, syllabus.extra_policies, ln=1)


        pdf.output('course.pdf', 'F')


    def pdf_read(filename):
        with open(filename, 'rb') as F:
            p = F.read()
            return p

    def pdf_store(filename, course_number, course_version):
        data = pdf_read(filename)
        query('UPDATE syllabus')
