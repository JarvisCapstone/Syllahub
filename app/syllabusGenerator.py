from fpdf import FPDF
from app import db
from app.models import Syllabus, SyllabusInstructorAssociation, Course, Instructor, Clo
from sqlalchemy_utils import Timestamp
from sqlalchemy import and_, Boolean, Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, MetaData, String, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import update
import os

class syllabusGenerator():
    
    #will complain if pdf name already exists
    def pdf_Generate(course_number=33211, course_version=1,
                     section=1, semester='summer', version=1, year=2019):

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
        #pdf=FPDF('P', 'in', 'A4')
        #pdf.set_margins(1, 1, 1)
        #pdf.set_auto_page_break(False, margin=0)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 5, 'CS' + str(course_number) + ' ' + course.name, ln=1, align='C')
        pdf.cell(0, 5, 'Course Syllabus', ln=1, align='C')
        pdf.ln(5)
        
        pdf.set_font_size(14)

        #TODO, once we find out relationships
        pdf.cell(0, 10, instructor.name, ln=1, align='C')
        pdf.ln(5)
        pdf.set_font('')
        pdf.cell(0, 5, semester + ' ' + str(year) + ' Semester', ln=1, align='C')
        #TODO, make section number a string in database, add check
        # for section to determine campus
        pdf.cell(0, 5, 'Kent Campus, Section: ' + str(section), ln=1, align='C')
        #pdf.ln(5)
        #TODO, fix once room number and building are moved to syllabus
        #TODO, revamp meeting_time once we get delimiter solved
        if (syllabus.meeting_time != None):
            pdf.cell(0, 5, syllabus.meeting_time + ', ' +
            str(course.room) + ' ' + course.building , ln=1, align='C')
        else:
            pdf.cell(0, 10, 'This is an online course, there is no meeting times',
                    ln=1, align='C')
        pdf.ln(10)
        pdf.set_font_size(14)

        #TODO, optional, once in db
        #if introduction != null:
        #pdf.cell(0,5, 'Instructor Introduction', ln=1)
        #pdf.set_font_size(12)
        #pdf.multi_cell(0,5, 'Walker is a very nice man who is teaching this course')
        #pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Contact Information', ln=1)
        #TODO, once we find out relations
        pdf.set_font_size(12)
        pdf.cell(0,5, 'Email: ' + instructor.email, ln=1)
        pdf.cell(0,5, 'Phone: ' + str(instructor.phone), ln=1)
        #TODO, include office room in database
        #pdf.cell(0,5, 'Office: #####', ln=1)
        pdf.cell(0,5, 'Office Hours: ' + instructor.perfered_office_hours, ln=1)
        pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Course Description from the University Catalog', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0,5, 'CS'+str(course_number) + ' ' + course.name + ': ' +
                course.description)    
        if (course.prerequisites != None):
            pdf.cell(0,5, 'Prerequisite: ' + course.prerequisites, ln=1)
            pdf.cell(0, 5, 'Students without the proper prerequisite(s) risk being deregistered from the class', ln=1)
        pdf.ln(5)

        pdf.set_font_size(14)
        pdf.cell(0,5, 'Course Learning Outcomes', ln=1)
        pdf.set_font_size(12)
        pdf.cell(0,5, 'By the end of this course, you should be able to:', ln=1)
        #TODO, for each clo in course
        # pdf.multi_cell(0,10, clo.general)

        if(course.is_core):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This coourse may be used to satisfy a Kent Core requirement. The Kent Core as a whole is intended to broaden intellectual perspectives, foster ethical and humanitarian values, and prepare students for responsible citizenship and productive careers.')
        if(course.is_diversity==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to satisfy the University Diversity requirement. Diversity courses provide opportunities for students to learn about such matters as the history, culture, values and notable achievements of people other than those of their own national origin, ethnicity, religion, sexual orientaiton, age, gender, physical and mental ability, and social class. Diversity courses also provide opportunities to examine problems and issues that may arise from differences, and opportunities to learn how to deal constructively with them.')
        if(course.is_wi==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to satisfy the Writing Intensive Course (WIC) requirement. The purpose of a writing-intensive course is to assist students in becoming effective writers within their major discipline. A WIC requires a substantial amount of writing, provides opportunities for guided revision, and focuses on writing forms and standards used in the professional life of the discipline.')
        if(course.is_elr==1):
            pdf.ln(5)
            pdf.multi_cell(0, 5, 'This course may be used to fulfill the university\'s Experiential Learning Requirement (ELR) which provides students with the opportunity to initiate lifelong learning through the development and application of academic knowledge and skills in new or different settings. Experiential learning can occur through civic engagement, creative and artistic activities, practical experiences, research, and study abroad/away.')
        
        #TODO, required should be moved to course, no syllabus
        if (syllabus.required_materials != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Required Materials', ln=1)
            pdf.set_font_size(12)
            pdf.multi_cell(0,5, syllabus.required_materials)
        if (syllabus.optional_materials != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Optional Materials', ln=1)
            pdf.set_font_size(12)
            pdf.cell(0,5, syllabus.optional_materials, ln=1)

        #TODO, enforce notnull dates / policies      
        pdf.ln(5)        
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Grading Policy', ln=1)
        pdf.multi_cell(0,5, syllabus.grading_policy)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Registration Date', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, 'University policy requires all students to be officially registered in each class they are attending. Students who are not officially registered for a course by published deadlines should not be attending classes and will not receive credit or a grade for the course. Each student must confirm enrollment by checking his/her class schedule (using Student Tools in FlashLine) prior to the deadline indicated. Registration errors must be corrected prior to the deadline.')
        pdf.cell(0,5, 'https://www.kent.edu/registrar/fall-your-time-register', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Withdrawl Date', ln=1)
        pdf.set_font_size(12)
        pdf.cell(0, 5, 'The course withdrawal deadline is', ln=1)
        pdf.cell(0,5, 'https://www.kent.edu/registrar/spring-important-dates', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Attendance Policy', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0,5, syllabus.attendance_policy)
        #pdf.cell(0,5, 'Attendance Policy goes here', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Student Accessability Services', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, syllabus.Students_with_disabilities)
        #pdf.cell(0,5, 'Important info here', ln=1)

        pdf.ln(5)
        pdf.set_font_size(14)
        pdf.cell(0,5, 'Academic Integrity', ln=1)
        pdf.set_font_size(12)
        pdf.multi_cell(0, 5, syllabus.University_cheating_policy)
        #pdf.cell(0,5, "Don't plagarize bad", ln=1)

        if (syllabus.extra_policies != None):
            pdf.ln(5)
            pdf.set_font_size(14)
            pdf.cell(0,5, 'Extra Policies', ln=1)
            pdf.set_font_size(12)
            pdf.multi_cell(0,5, syllabus.extra_policies)
        

        pdf.output('course.pdf', 'F')


    def pdf_store(filename = 'course.pdf', course_number = 33211, course_version=1):
        file = open('course.pdf', 'rb').read()
        db.session.query(Syllabus) \
            .filter_by(course_number=course_number, course_version=course_version) \
            .update({"pdf": (file)})
        db.session.commit()

    def pdf_delete(filename = 'course.pdf'):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File doesn't exist")