from fpdf import FPDF
from app import db
from app.models import Syllabus

class syllabusGenerator():
    
    def pdfGenerate(syllabus):

        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'CS' + str(syllabus.course_number), ln=1, align='C')
        pdf.cell(0, 10, 'Course Syllabus', ln=1, align='C')
        pdf.ln(5)

        pdf.set_font_size(10)

        #TODO, once we find out relationships
        for instructor in syllabus.instructorList
            pdf.cell(0, 10, instructor.name, ln=1, align='C')
        pdf.ln(5)
        pdf.cell(0, 10, syllabus.semester + ' ' + str(syllabus.year) + ' Semester', ln=1, align='C')
        #TODO, make section number a string in database, add check
        # for section to determine campus
        pdf.cell(0, 10, 'Kent Campus, Section: ' + str(syllabus.section), ln=1, align='C')
        pdf.ln(5)
        #TODO, fix once room number and building are moved to syllabus
        #TODO, revamp meeting_time once we get delimiter solved
        if (syllabus.meeting_time != None):
            pdf.cell(0, 10, 'Meetings Times: '+ syllabus.meeting_time + ', ' +
            str(syllabus.course.room) + ' ' + syllabus.course.building , ln=1, align='C')
        else:
            pdf.cell(0, 10, 'This is an online course, there is no meeting times',
                     ln=1, align='C')
        pdf.ln(10)
        for instructor in syllabus.instructorList:
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
        pdf.cell(0,10, 'CS'+str(syllabus.course_number) + ' ' + syllabus.course.name + ': ' +
                 syllabus.course.description, ln=1)    
        if (syllabus.course.prerequisites != None):
            pdf.cell(0,10, 'Prerequisite: ' + syllabus.course.prerequisites, ln=1)
        pdf.ln(5)

        pdf.cell(0,10, 'Course Learning Outcomes', ln=1)
        pdf.cell(0,10, 'By the end of this course, you should be able to:', ln=1)

        for clo in syllabus.course.clos
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
