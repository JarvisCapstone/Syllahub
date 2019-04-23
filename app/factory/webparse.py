#import requests

# https://www.kent.edu/cs/office-hours Table for office hours
import pandas as pd
import pprint
from app.models import Course, Syllabus
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

        #for index, row in table.iterrows():
        #    print('--------------------------------------------------')
        #    print(row)


        # remove first row because this is the column headdings
        return table
        #return tables[0] #table is now a dataframe object

    
    def getCourseDetails(self):
        #details = pd.read_html('http://catalog.kent.edu/colleges/as/cs/')
        from lxml import html
        import requests
        page = requests.get('http://catalog.kent.edu/colleges/as/cs/')
        tree = html.fromstring(page.content)
        print(tree)
        block = tree.xpath('//div[@class="sc_sccoursedescs"]/text()')
        print(block)


    def iterate(self):
        for index, row in self.tableDataFrame.iterrows():
            #print(row)
            print(row.Crse)

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
        return 'done'

    def run(self):
        self.setInstructors()

        syllabusTable = self.getSyllabusTable()
        grouped = self.groupSyllabusDataFrame(syllabusTable)
        #r = grouped.iloc[0]
        #print(r)
        #print('------------------------------------------------------')


        # Create instructor
        #print(type(r.Instructor))
        #for instructor in r.Instructor:
            #print('type=', type(instructor))
            # instructors in the list are usually strings or floats = to 'nan'. 
            # If the input is a string, it is probably a correct instructor. 
            #if type(instructor) is str:
                #print('instructor=', instructor)
                #print
        
        for index, row in grouped.iterrows():
            #    print(index)
            #    #row is a series type
            #x = row.to_dict()
            #See if Course already exists in db. 
            # Primary key is course.number
            # data from web is a string of the format "CS #####" where # are the numbers we want

            numberString = row.Crse[-5:] # selects only the 5 rightmost charicters 
            course_number = int(numberString)
            course = CourseFactory.createOrGet(number=course_number,
                                               version='any')

            CourseFactory.updateIfDifferent(course, name=row.Title)
            # Create Syllabus if it doesn't already exits
            # syllabus primary key 
            #     course_number = Column(Integer, primary_key=True)
            #     course_version = Column(Integer, primary_key=True)
            
            #     section = Column(Integer, primary_key=True) # TODO change to string(3)
            #     semester = Column(Enum('spring', 'summer', 'fall'), primary_key=True)
            #     version = Column(Integer, primary_key=True)
            #     year = Column(Integer, primary_key=True)
            section = row.Sec
            yearAndSemester = row.Semester # has both info Ex: "2019 Spring"
            yearString = yearAndSemester[:4] # get left 4 chars
            year = int(yearString)
            semester = yearAndSemester[5:] # get chars after char 5
            #print('name=', newCourse.name)
            # TODO, figure out how we will do time and loc information
            #locationList = r.Loc
            #BuildingStr = ""
            #timeStr = 
            #for location in locationList
            #    locationStr += location
            sF = SyllabusFactory()
            syllabus = sF.createOrGet(course_number=course.number,
                                      course_version=course.version,
                                      section=section,
                                      semester=semester,
                                      year=year,
                                      version='any')
            meeting_time = 'ToDo'
            SyllabusFactory.updateIfDifferent(syllabus, meeting_time) #TODO. once time format is setup
