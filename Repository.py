"""Homework 12
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 08/12/2018"""

# ----------
# Repository Class: Storage of all data for the Course Tracker System
# ----------

import os
import sys
import sqlite3

from Student import Student
from Instructor import Instructor
from Major import Major
from prettytable import PrettyTable
from flask import Flask, render_template

app = Flask(__name__)

class Repository:
    '''Encapsulates the data needed and managed by the Course Tracker System.
       Will utilize the Repository.db database file in the specified path
       or the current working directory.'''

    def __init__(self, path=""):
        '''Initialize an empty repository'''
        self._students = {}
        self._instructors = {}
        self._majors = {}
        if path != "":
            self.load_from_path(path)

    def load_students(self):
        '''Load the students data from the database.'''
        try:
            students = self._db.execute("select CWID, NAME, MAJOR from STUDENTS")
        except sqlite3.OperationalError:
            print("Unable to load the students data from the database.")
        else:
            for id, name, major in students:
                self._students[id] = Student(id, name, major)

    def load_instructors(self):
        '''Load the instructors data from the database.'''
        try:
            instructors = self._db.execute("select CWID, NAME, DEPT from INSTRUCTORS")
        except sqlite3.OperationalError:
            print("Unable to load the instructors data from the database.")
        else:
            for id, name, dept in instructors:
                self._instructors[id] = Instructor(id, name, dept)

    def load_grades(self):
        '''Load the grades data from the database and process them.'''
        try:
            grades = self._db.execute("select STUDENT_CWID, COURSE, GRADE, INSTRUCTOR_CWID from GRADES")
        except sqlite3.OperationalError:
            print("Unable to load the grades data from the database.")
        else:
            for s_id, course, grade, i_id in grades:
                if s_id in self._students.keys():
                    self._students[s_id].add_grade(course, grade)
                if i_id in self._instructors.keys():
                    self._instructors[i_id].increment_student_count(course)

    def load_majors(self):
        '''Load the major definitions (required and elective courses) and process them.'''
        try:
            majors = self._db.execute("select MAJOR, COURSE_TYPE, COURSE from MAJORS")
        except sqlite3.OperationalError:
            print("Unable to load the majors data from the database.")
        else:
            for major, course_type, course in majors:
                for s in self._students.keys():
                    if course_type == 'R' and self._students[s]._major == major:
                        self._students[s].add_required_course(course)
                    if course_type == 'E' and self._students[s]._major == major:
                        self._students[s].add_elective_course(course)
                if major not in self._majors.keys():
                    self._majors[major] = Major(major)
                self._majors[major].add_course(course, course_type)

    def load_from_path(self, path):
        '''Read the data from the database in the specified path into the objects/structures'''
        db_path = os.path.join(path,"repository.db")
        self._db = sqlite3.connect(db_path)
        self.load_students()
        self.load_instructors()
        self.load_grades()
        self.load_majors()

    def print_students(self):
        pt = PrettyTable(field_names=['CWID','Name','Major','Completed Courses','Remaining Required','Remaining Electives'])
        for s in self._students.keys():
            pt.add_row(self._students[s].prettyprint())
        return pt

    def print_instructors(self):
        pt = PrettyTable(field_names=['CWID','Name','Dept','Course','Students'])
        for i in self._instructors.keys():
            for pp in self._instructors[i].prettyprint():
                pt.add_row(pp)
        return pt

    def print_majors(self):
        pt = PrettyTable(field_names=['ID','Required Courses','Elective Courses'])
        for m in self._majors.keys():
            pt.add_row(self._majors[m].prettyprint())
        return pt
        
    def load_instructors_detail(self):
        '''Return the instructors listing with the course count for each instructor.'''
        sql = '''select I.CWID, I.NAME, I.DEPT, G.COURSE, count(G.STUDENT_CWID) as 'STUDENTS'
                 from INSTRUCTORS I join GRADES G on I.CWID=G.INSTRUCTOR_CWID
                 group by G.COURSE order by I.NAME asc, G.COURSE asc'''
        try:
            instructors = self._db.execute(sql)
        except sqlite3.OperationalError:
            print("Unable to build the instructors detail data from the database.")
        else:
            return [{'cwid':id, 'name':name, 'dept':dept, 'course':course, 'students':students} \
                    for id, name, dept, course, students in instructors]
                    
    def close(self):
        '''Close the connection to the database.'''
        self._db.close()
        
@app.route("/")
def hello():
    '''Test to ensure that Flask is running and bound to the code correctly.'''
    return "Hello, world! This is Flask!"
    
@app.route("/instructors")
def render_instructors():
    '''Render the detailed instructors table response.'''
    repo = Repository(os.getcwd())
    data = render_template("Instructors.html", \
                           title="Instructors Detail", \
                           table_title="Instructors Detail", \
                           instructors=repo.load_instructors_detail())
    repo.close()
    return data

def validate_arguments():
    '''Validate the command line arguments.'''
    if len(sys.argv) > 2:
        # Invalid syntax - provide correct syntax and exit.
        print("Invalid syntax.")
        print("python Repository.py [path to database excluding database file name]")
        quit()

    # Default to current working directory unless the user provides another directory.
    path = os.getcwd()
    if len(sys.argv) == 2:
        path = sys.argv[1]
    return path

if __name__ == '__main__':
    # Load the repository data.
    # repo = Repository(validate_arguments())

    # Print the Majors, Students and Instructors in PrettyTables.
    # print(repo.print_majors())
    # print(repo.print_students())
    # print(repo.print_instructors())
    
    app.run(debug=True)
    