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
    tableDataFrame = ''
    def getTable(self):
        tables = pd.read_html('https://web.cs.kent.edu/schedule/', 
                              header=0)
        self.tableDataFrame = tables[1] #table is now a dataframe object
    
    def printTable(self):
        print(tableDataFrame)
        #tableJSON = tableDataFrame.to_json(orient="records")
        #pprint(tableJSON)

    def iterate(self):
        for index, row in self.tableDataFrame.iterrows():
            #print(row)
            print(row.Crse)

    def group(self):
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
        group = self.tableDataFrame.groupby('CRN').aggregate(aggregation_functions)
        return group

    def run(self):
        self.getTable()
        grouped = self.group()
        #r = grouped.iloc[0]
        #print(r)
        #print('------------------------------------------------------')

        '''
        # Create instructor
        print(type(r.Instructor))
        for instructor in r.Instructor:
            print('type=', type(instructor))
            # instructors in the list are usually strings or floats = to 'nan'. 
            # If the input is a string, it is probably a correct instructor. 
            if type(instructor) is str:
                print('instructor=', instructor)
                #print

        '''
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
            syllabus = SyllabusFactory.createOrGet(course_number=course.number,
                                                   course_version=course.version,
                                                   section=section,
                                                   semester=semester,
                                                   year=year,
                                                   version='any')
            meeting_time = 'ToDo'
            SyllabusFactory.updateIfDifferent(syllabus, meeting_time) #TODO. once time format is setup
        
