#TASK 3 
import pandas as pd

df = pd.read_csv("./csv/employees.csv")

list_of_employees = [row['first_name'] + " " + row['last_name'] for index, row in df.iterrows()]
print(list_of_employees)

names_with_e = [name for name in list_of_employees if 'e' in name.lower()]
print(names_with_e)
