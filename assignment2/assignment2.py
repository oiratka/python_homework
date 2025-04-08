from datetime import datetime

import csv
import traceback
import os
import custom_module

#Task 2 Read a CSV file
employees_data = {}

def read_employees ():
    try:
        dict_data = {}#empty dict for key/values
        list_data = []#empty list to store rows
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)# get the first row
            dict_data['fields'] = header

            for row in reader:
                list_data.append(row)
            
            dict_data['rows'] = list_data
            global employees_data
            employees_data = dict_data
            return dict_data

    except Exception as e:
     trace_back = traceback.extract_tb(e.__traceback__)
     stack_trace = [
        f'File : {trace[0]} , Line : {trace[1]}, Func : {trace[2]}, Message : {trace[3]}'
        for trace in trace_back
        ]

    print(f"Exception type: {type(e).__name__}")
    print(f"Exception message: {str(e)}")
    print(f"Stack trace: {stack_trace}")

    exit (1)

employees = read_employees()
print(employees)

#Test 3 Find the column index

global employee_id_column

def column_index (column_name):
   return employees_data['fields'].index(column_name)

read_employees()
employee_id_column = column_index('employee_id')

print (f"'employee_id' column_index: {employee_id_column}")

#Task 4 Find the employee first name

def first_name (row_number):
   first_name_column = column_index("first_name")
   row = employees_data['rows'][row_number-1]
   return row[first_name_column]

print(first_name(2))
   
#Task 5 Find an employee
def employee_find (employee_id):
   employee_id_column = column_index('employee_id')

   def employee_match(row):
      return int(row[employee_id_column]) == employee_id
   
   matches = list(filter(employee_match, employees['rows']))
   return matches


#Task 6 Find employee with a lamda

def employee_find_2(employee_id):
   matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees['rows']))
   return matches

#Task 7 sort the rows by last_name using a Lambda

def sort_by_last_name():
   last_name_column = column_index('last_name')
   employees['rows'].sort(key = lambda row: row[last_name_column])

   return employees['rows']

#Task 8 Create a dict for an employee

def employee_dict(row):
   employee_info = {
      employees_data['fields'][i]: row[i] for i in range(len(employees['fields']))
      if employees['fields'][i] != 'employee_id'
   }

   return employee_info

# Task 9 A dict of dicts for all employees

def all_employees_dict():
   all_employees_info = {
      row[0]: employee_dict(row)
      for row in employees['rows']
   }
   return all_employees_info

# Task 10 use of os module

def get_this_value():
   value = os.environ.get('THISVALUE') 
   return value


#Task 11 Creating your own module

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("no more secrets")

print(custom_module.secret)

#Task 12 Read minutes
def read_minutes ():
   minutes1 = {}
   minutes1_rows = []
   minutes2 = {}
   minutes2_rows = []
   with open ('../csv/minutes1.csv') as file1, open('../csv/minutes2.csv') as file2:
      reader1 = csv.reader(file1)
      reader2 = csv.reader(file2)

      header1 = next(reader1)
      header2 = next(reader2)

      minutes1['fields'] = header1
      minutes2['fields'] = header2

      for row1, row2 in zip(reader1, reader2):
         minutes1_rows.append(tuple(row1))
         minutes2_rows.append(tuple(row2))
         
         minutes1['rows'] = minutes1_rows
         minutes2['rows'] = minutes2_rows
      
   return minutes1, minutes2

minutes1, minutes2 = read_minutes()

print("Minutes1:", minutes1)
print("Minutes2:", minutes2)

#Task 13 Create minutes_set

def create_minutes_set():
   minutes1_set = set(
      (row[minutes1['fields'].index('Name')], row[minutes1['fields'].index('Date')])
   for row in minutes1['rows']
   )
   minutes2_set = set(
      (row[minutes2['fields'].index('Name')], row[minutes2['fields'].index('Date')])
    for row in minutes2['rows']
   )
   minutes_set = minutes1_set | minutes2_set
   return minutes_set

#Task 14 Convert to daytime
def create_minutes_list():
   global minutes_list
   new_list = list(minutes_set)
   minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),new_list))
   return minutes_list

minutes_set = create_minutes_set()
minutes_list = create_minutes_list()
print(minutes_list)

#Test 15 Write out sorted list

def write_sorted_list():
   sorted_list = sorted(minutes_list, key = lambda x: x[1])
   sorted_list_string = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), sorted_list))

   with open('./minutes.csv', mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(minutes1['fields'])

      for row in sorted_list_string:
         writer.writerow(row)
   return sorted_list_string
      
write_sorted_list()
