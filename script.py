#!/usr/bin/env python
# coding: utf-8
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
for row in fcsv:
    if first:
        classes = row
        for i in classes:
            tutor_classes[i] = []
        first = False
        continue
    index = -1
    for name in row:
        index += 1
        if name != "":
            if classes[index] == "Other":
                continue
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
day = "NaN"
for row in fcsv:
    if first:
        tutors = row
        for i in tutors:
            if first:
                first = False
                continue
            if i != "":
                tutor_hours[i] = []
        continue
    if row[0] != "":
        day = row[0]
    shift = row[1]
    index = -1
    for i in row:
        index += 1
        if index < 2:
            continue
        if i != "":
            tutor_hours[tutors[index]].append(day + ", " + shift)
hours.close()



##########################################################
### Find shifts where there is a tutor on duty for a class
##########################################################

class_hours = dict()
errors = dict()
for key, value in tutor_classes.items():
    class_hours[key] = []
    errors[key] = []
    for tutor in value:
        try:
            tutor_hours[tutor]
            temp_hours = tutor_hours[tutor]
            for cur_shift in temp_hours:
                if cur_shift not in class_hours[key]:
                    class_hours[key].append(cur_shift)
        except:
            errors[key].append(tutor)

######################################
### Sort hours by day and then by time
######################################

class_hours_sorted = dict()
for course, shifts in class_hours.items():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    course_shifts = []
    for day in days:
        day_shift_list = []
        for i in shifts:
            if day in i:
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
                      
        combined_string = '\t'.join(day_shift_list)
        for shift in shift_list:
            if shift in combined_string:
                course_shifts.append([day,shift])
    class_hours_sorted[course] = course_shifts




###################################################################
### Placeholder generate HTML code until there is a better solution
###################################################################

for course, shifts in class_hours_sorted.items():
    shift_table = ""
    for shift in shifts:
        shift_table += """<tr><td>"""+shift[0]+"""</td><td>"""+shift[1]+"""</td></tr>
                          """
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
    
    ### Write to file
    html_file = open("HTML Output/"+course+".html","w")
    html_file.write(html)
    html_file.close()

print("Script execution complete. Have a nice day!")
