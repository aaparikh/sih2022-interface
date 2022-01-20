import pandas as pd
import numpy as np
#Use Sr. No. as a filter
df = pd.read_html("https://sih.gov.in/sih2022PS")[0]
print(df.columns)
# print(df['Category'].values)
print(df['Description & Briefs'].values[0])
#str.find returns the lowest index of found element in string
#elements to search are - Background, Summary, Objective
backgrounds = []
summary = []
objectives = []
# for desc in df['Description & Briefs']:
#     fbkg = desc.find('Background')
#     fsum = desc.find('Summary')
#     fobj = desc.find('Objective')

print(df['Sr. No.'].values[0])
#deal with mutilple Sr. No.
def range_to_search(inputtext):
    if(inputtext.contains('-')):
        #split by '-'
        #split by ' '
        #convert to int
        #return min and max
        pass
    elif(inputtext.contains(',')):
        #strip
        #split by ','
        # convert to a list
        # return this list
    elif(check if its a number):
        # return this number as a range from start and end as this number
    else:
        # return empty list