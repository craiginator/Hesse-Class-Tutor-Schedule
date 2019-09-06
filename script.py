#!/usr/bin/env python
# coding: utf-8
#author: Craig Behnke
#github.com/craiginator
#craig.behnke@valpo.edu
import csv

print("Executing script...\n\tPlease wait...")
######################################
### Get tutors for each tutored course
######################################

try:
    file = open("Input Data/Tutor Classes.csv")
except:
    print("ERROR: Tutor Classes.csv not found.")
    raise(Exception)
fcsv = csv.reader(file)
first = True

#Define data structure:
#Dict with the name of the course as a key, array of tutors as value
classes = []
tutor_classes = dict()
#Iterate through rows in the file
for row in fcsv:
    if first:  #If the row is the header row
        classes = row
        for i in classes:
        		#Create a dict with entries for each class and an empty list for names
            tutor_classes[i] = []
        first = False
        continue
    index = -1
    #Iterate through the columns in the row
    for name in row:
        index += 1
        #Check that the field contains a name
        if name != "":
            if classes[index] == "Other":
            		#'Other' entries are ignored
                continue
            #Add the name to the list of tutors for that course
            tutor_classes[classes[index]].append(name)
file.close()

####################################
### Get Working Hours for Each Tutor
####################################

try:
    hours = open("Input Data/Tutor Shifts.csv")
except:
    print("ERROR: Tutor Shifts.csv file not found.")
    raise(Exception)
fcsv = csv.reader(hours)
first = True
#Data structure is dict w/ tutor as key, array of times as value
tutor_hours = dict()
## tutors starts from index 2
tutors = []
#´day´ contains the most recently listed day in the file
day = "NaN"
for row in fcsv:
    if first: #if headers row
        #get a list with each tutor in the order they appear in
        tutors = row
        first = False
        for i in tutors:
        		#Iterate through the tutor names
            if i != "":
            		#Create a dict entry for each tutor
                tutor_hours[i] = []
        continue #stop processing header row
    
    if row[0] != "": #Check for new ´day´ entry
        day = row[0]
    #Get the shift for the row
    shift = row[1]
    index = -1
    #Iterate through entries in the row
    for i in row:
        index += 1
        if index < 2: #Skip over day and shift fields
            continue
        if i != "": #If a name exists
        		#Add an entry in the tutor_hours dict that this tutor works this shift
            tutor_hours[tutors[index]].append(day + ", " + shift)
hours.close()



##########################################################
### Find shifts where there is a tutor on duty for a class
##########################################################

class_hours = dict()
errors = dict()
#Iterate through classes and the associated list of tutors
for key, value in tutor_classes.items():
		#Create empty entry for this course
    class_hours[key] = []
    errors[key] = []
    #Iterate through names of tutors who can tutor the current course
    for tutor in value:
        try:
        		#Check that the tutor name exists (there may be a typo or something)
        		#If not, it aborts name processing and makes an entry in the 'errors' dict
            tutor_hours[tutor]
            #Add that tutor's hours to the temp_hours list
            temp_hours = tutor_hours[tutor]
            
            #Check for duplicates between the current tutor´s shifts and the shifts already associated with the course
            for cur_shift in temp_hours:
                if cur_shift not in class_hours[key]:
                		#add current shift to list of class's shifts
                		class_hours[key].append(cur_shift)
        except:
        		#append that tutor name to the errors for that course
            errors[key].append(tutor)

######################################
### Sort hours by day and then by time
######################################

class_hours_sorted = dict()
#Iterate through courses and associated lists of shifts (unsorted)
for course, shifts in class_hours.items():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    course_shifts = []
    #Find shifts in each successive day
    for day in days:
        day_shift_list = []
        #Iterate through all of the class´s shifts
        for i in shifts:
        		#Check that the current day is found in that specific shift
            if day in i:
            #Add the shift to an intermediate list
                day_shift_list.append(i)
        shift_list = ["10:25a-11:25a",
                     "11:25a-12:25p",
                     "12:25p-1:25p",
                     "1:25p-2:25p",
                     "2:00p-3:00p",
                     "2:25p-3:25p",
                     "3:00p-4:00p",
                     "3:25p-4:25p",
                     "4:00p-5:00p",
                     "4:25p-5:25p",
                     "7:00p-8:00p",
                     "8:00p-9:00p",
                     "9:00p-10:00p"]
        
        #Combine all of the day´s shifts into a single string for str search purposes
        combined_string = '\t'.join(day_shift_list)
        #Iterate through the entire universe of possible shifts
        for shift in shift_list:
        		#If that shift exists
            if shift in combined_string:
            		#Append it to the final list of shifts for that course
                course_shifts.append([day,shift])
    #Save the list to the dict under the course name
    class_hours_sorted[course] = course_shifts




###################################################################
### Placeholder generate HTML code until there is a better solution
###################################################################

#Iterate through all covered courses
for course, shifts in class_hours_sorted.items():
    shift_table = ""
    #Create an HTML table row for each shift
    for shift in shifts:
        shift_table += """<tr><td>"""+shift[0]+"""</td><td>"""+shift[1]+"""</td></tr>
                          """
    #Generate the overall HTML document
    html = '''<doctype html>
              <html lang="en-US">
              <head>
                  <meta charset="utf-8">
                  <title>'''+course+''' Tutoring Hours</title>
                  <meta name="description" content="List of Hours where '''+course+''' is tutored in the Hesse Center">
                  <meta name="author" content="Valparaiso University Hesse Center -- Designed by Students">
             </head>
             <body>
                 <h1>'''+course+''' Tutoring Hours</h1>
                 <table>
                     <tr><th>Day</th><th>Shift Time</th></tr>
                     '''+shift_table+'''
                 </table>
             </body>'''
    
    ### Write that course´s HTML to output file
    html_file = open("HTML Output/"+course+".html","w")
    html_file.write(html)
    html_file.close()

print("Script execution complete. Have a nice day!")
