#import requests

# https://www.kent.edu/cs/office-hours Table for office hours
import pandas as pd
import pprint
from app.models import Course, Syllabus, Instructor
from app.factory.factory import InstructorFactory, CourseFactory, SyllabusFactory
from app import db

class Retriever():
    '''Read cs courses from a table on their website
    '''
    def getSyllabusTable(self):
        tables = pd.read_html('https://web.cs.kent.edu/schedule/', 
                              header=0)
        # the first table on the page is not needed
        return tables[1] #table is now a dataframe object

    def getInstructorTable(self):
        data = pd.read_html('https://www.kent.edu/cs/office-hours', 
                              header=0)
        #print(data)
        table = data[0] # the data we want is the first table on the page
        
        # Rename columns because Kent's table format is terrible
        table.columns = ['name', 'office', 'phoneEnding', 'officeHours', 'email']

        # Remove useless data
        for index, row in table.iterrows():
            if row['name'] == 'Name': # Row with column names as data
                table.drop(index, inplace=True)
            elif 'Office Hours' in row['name']: # Row with table title as data
                table.drop(index, inplace=True)

        # remove first row because this is the column headings
        return table

    
    def getCourseDetails(self):
        #details = pd.read_html('http://catalog.kent.edu/colleges/as/cs/')
        #from lxml import html
        #import requests
        #page = requests.get('http://catalog.kent.edu/colleges/as/cs/')
        #tree = html.fromstring(page.content)
        #print(tree)
        #block = tree.xpath('//div[@class="sc_sccoursedescs"]/text()')
        #print(block)
        pass

    def groupSyllabusDataFrame(self, table):
        aggregation_functions = {
            'Crse': 'first', 
            'Sec': 'first',
            'Cred': 'first',
            'Title': 'first',
            'Semester': 'first',
            'Days': lambda x: x.tolist(),
            'Instructor': lambda x: x.tolist(),
            'Loc': lambda x: x.tolist(),
            'Time': lambda x: x.tolist(),
        }
        group = table.groupby('CRN').aggregate(aggregation_functions)
        return group

    def runTest(self):
        self.getCourseDetails()

    def setInstructors(self):
        instructorTable = self.getInstructorTable()
        # add instructors in this table to Instructors
        iFactory = InstructorFactory()
        for index, row in instructorTable.iterrows():
            data = {}
            data['name'] = row['name']
            data['email'] = row['email']
            data['perfered_office_hours'] = row['officeHours']
            phoneEnding = row['phoneEnding']
            # ensure phone was provided and is of the appropreate length
            if isinstance(phoneEnding, str):
                if len(phoneEnding) == 5:
                    # 330-67#-#### is the kent phone number format
                    phoneString = '33067' + phoneEnding 
                    data['phone'] = int(phoneString)
            i = iFactory.createOrGet(data)
            i.updateIfDifferent(data)
        
        # The data online is somewhat incomplete. I manually entered in 
        # a few faculty below.
        additionalInstructors = [
            {
                'email':'dcsmith1@kent.edu',
                'phone': 3306720275,
                'name': 'Smith, Deborah C.',
            },
        ]
        
        for instructorData in additionalInstructors:
            i = iFactory.createOrGet(instructorData)
            i.updateIfDifferent(instructorData)
        return 'done'

    def run(self):
        self.setInstructors()

        syllabusTable = self.getSyllabusTable()
        grouped = self.groupSyllabusDataFrame(syllabusTable)

        
        for index, row in grouped.iterrows():
            #See if Course already exists in db. 
            # Primary key is course.number
            # data from web is a string of the format "CS #####" where # are the numbers we want

            numberString = row.Crse[-5:] # selects only the 5 rightmost charicters 
            course_number = int(numberString)
            course = CourseFactory.createOrGet(number=course_number,
                                               version='any')

            CourseFactory.updateIfDifferent(course, name=row.Title)
            # Create Syllabus if it doesn't already exits
            section = row.Sec
            yearAndSemester = row.Semester # has both info Ex: "2019 Spring"
            yearString = yearAndSemester[:4] # get left 4 chars
            year = int(yearString)
            semester = yearAndSemester[5:] # get chars after char 5
            
            sF = SyllabusFactory()
            syllabus = sF.createOrGet(
                              course_number=course.number,
                              course_version=course.version,
                              section=section,
                              semester=semester,
                              year=year,
                              version='any')

            for instructorName in row.Instructor:
                i = None
                if isinstance(instructorName, str):
                    i = Instructor.query.filter_by(name=instructorName).first()
                    if not i:
                        # Our database seeding information is terrible. Since I
                        # don't have time to write  neural network to detect 
                        # simmilar sounding names, This whitelist will have
                        # to do
                        simmilarNames = {
                            'Allouzi, Maha A.': 'Allouzi, Maha',
                            'Bansal, Arvind K.':'Bansal, Arvind', 
                            'DeLozier, Gregory S.': 'DeLozier, Greg',
                            'Dragan, Feodor F.': 'Dragan, Feodor',
                            'Ghazinour Naini, Kambiz': 'Ghazinour, Kambiz',
                            'Guarnera, Heather M.':'Guarnera, Heather',
                            'Haverstock, William D.':'Haverstock, Dale', 
                            'Hossain, Md Amjad':'Hossain, Amjad Md',
                            'Lu, Cheng-Chang':'Lu, C.C.',
                            'Maletic, Jonathan I.': 'Maletic, Jonathan',
                            'Peyravi, Hassan M.': 'Peyravi, Hassan',
                            'Samba, Augustine S.': 'Samba, Gus',
                            'Volkert, L G.': 'Volkert, L. Gwenn',
                            'Walker, Robert A.':'Walker, Robert',
                        }
                        if instructorName in simmilarNames:
                            i = Instructor.query.filter_by(
                                name=simmilarNames[instructorName]).first()
                        else:
                            # TODO
                            # Carl, Michael and Al Thoubi, Assad Y. are present
                            # in one table but not the other. I ignored them 
                            # for now. Sorry Carl and Al
                            pass
                if i:
                    syllabus.addInstructor(i, 'instructor')

            meeting_time = 'ToDo'
            SyllabusFactory.updateIfDifferent(syllabus, meeting_time) #TODO. once time format is setup
