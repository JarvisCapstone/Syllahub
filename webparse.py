#import requests
import pandas as pd
import pprint

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

        #print(group)
        #for index, row in group.iterrows():
        #    #print(row)
        #    print(row)
        return group

    def run(self):
        self.getTable()
        grouped = self.group()
        #print(type(grouped))
        for index, row in grouped.iterrows():
            #print(row)
            #row is a series type
            x = row.to_dict()
            print(x)
            #TODO convert this into models of courses and syllabi and add them to the DB


a = Retriever()
a.run()
