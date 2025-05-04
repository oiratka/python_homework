import sqlite3

#SECOND EXAMPLE 7.4
#fn to add a student into Students table; 
def add_student(cursor, name, age, major):
    try:
        cursor.execute("INSERT INTO Students (name, age, major) VALUES (?,?,?)", (name, age, major))
    except sqlite3.IntegrityError:
        print(f" {name} is already in the DB.")

def add_course(cursor, name, instructor):
    try:
        cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES (?,?)", (name, instructor))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the DB")

def enroll_student(cursor, student, course):
        cursor.execute("SELECT * FROM Students WHERE name = ?", (student,))# for a tuple with one element we need to include comma
        results = cursor.fetchall()
        if len(results) > 0:
            student_id = results[0][0]
        else:
            print(f"There was no student named {student}")
            return
        cursor.execute('SELECT * FROM Courses WHERE course_name = ?', (course, ))
        results = cursor.fetchall()
        if len(results) > 0:
            course_id = results [0][0]
        else:
            print(f"There was no course named {course}")
            return
        cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?,?)", (student_id, course_id))
        cursor.execute("SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        results = cursor.fetchall()
        if len(results) >0:
            print(f"Student {student} is already in course {course}")
            return


with sqlite3.connect("../db/school.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()


    

    add_student(cursor, 'Alice', 20, "Computer science")
    add_student(cursor, 'Bob', 22, "History")
    add_student(cursor, 'Charlie', 19, "Biology")
    add_student(cursor, 'Marina', 39, "Python")
    add_course(cursor, 'Math 101', 'Dr. Smith')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')
    enroll_student(cursor, "Alice", "Math 101")
    enroll_student(cursor, "Alice", "Chemistry 101")
    enroll_student(cursor, "Bob", "Math 101")
    enroll_student(cursor, "Bob", "English 101")
    enroll_student(cursor, "Charlie", "English 101")

    conn.commit()
    print("Sample data inserted successfully!")



    
