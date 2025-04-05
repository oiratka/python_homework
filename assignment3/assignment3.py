import pandas as pd
import json

#Task 1 creating and manipulating data
data_set = {
    'Name':['Alice', 'Bob', 'charlie'],
    'Age': [25,30,35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(data_set)
print(task1_data_frame)

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print(task1_with_salary)

task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print(task1_older)

task1_older.to_csv('employees.csv', index = False)

#Task2 load data from csv and JSON
task2_employees = pd.read_csv('employees.csv')
print(task2_employees)

json_employees_data  = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000},
]

with open ('additional_employees.json', 'w') as file:
    json.dump(json_employees_data, file, indent=4)

json_employees = pd.read_json('additional_employees.json')
print(json_employees)

more_employees = pd.concat([task2_employees, json_employees], ignore_index = True)

#Task3 data inspection using head, tail, & info methods

first_three = more_employees.head(3)
print(first_three)

last_two = more_employees.tail(2)
print(last_two)

employee_shape = more_employees.shape
print(employee_shape)

more_employees.info()

#Task4 data cleaning

dirty_data = pd.read_csv('dirty_data.csv')
print(dirty_data)

clean_data = dirty_data.copy()

clean_data.drop_duplicates(inplace=True)
print(clean_data)

clean_data[["Age", "Salary"]] = clean_data[["Age", "Salary"]].replace("unknown", pd.NA)
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
print(clean_data)

#clean_data["Salary"] = clean_data["Salary"].replace("unknown", pd.NA)
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
print(clean_data)

clean_data.fillna(value={
    "Age":clean_data["Age"].mean(), 
    "Salary": clean_data["Salary"].median()
    }, inplace=True)
print(clean_data)

clean_data["Hire Date"] = pd.to_datetime(clean_data['Hire Date'], errors = "coerce")
print(clean_data)

clean_data["Name"] = clean_data["Name"].str.strip().str.upper()
clean_data["Department"] = clean_data["Department"].str.upper()
print(clean_data)

