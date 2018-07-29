"""Homework 10
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 07/29/2018"""

# ----------
# Repository Class: Storage of all data for the Course Tracker System
# ----------

import os
import sys

from Student import Student
from Instructor import Instructor
from Major import Major
from prettytable import PrettyTable

def line_values(path, num_fields, separator=",", header=False):
    '''Generator to yield the values in the next line of text in a file as a list'''
    try:
        fp = open(path,"r")
    except:
        raise FileNotFoundError
    else:
        with fp:
            for line_counter, line in enumerate(fp):
                if line_counter == 0 and header:
                    continue
                vals = line.rstrip().split(separator)
                if len(vals) != num_fields:
                    raise ValueError("'{}' has {} fields on line {} but expected {}".format( \
                        path,len(vals),line_counter,num_fields))
                yield vals
                
class Repository:
    '''Encapsulates the data needed and managed by the Course Tracker System'''

    def __init__(self, path=""):
        '''Initialize an empty repository'''
        self._students = {}
        self._instructors = {}
        self._majors = {}
        if path != "":
            self.load_from_path(path)

    def load_students(self, file):
        '''Load the students data from the specified file.'''
        try:
            for id, name, major in line_values(file, 3, "\t"):
                self._students[id] = Student(id, name, major)
        except FileNotFoundError:
            print("Error: Students file {} was not found.".format(file))

    def load_instructors(self, file):
        '''Load the instructors data from the specified file.'''
        try:
            for id, name, dept in line_values(file, 3, "\t"):
                self._instructors[id] = Instructor(id, name, dept)
        except FileNotFoundError:
            print("Error: Instructors file {} was not found.".format(file))

    def load_grades(self, file):
        '''Load the grades data from the specified file and process them.'''
        try:
            for s_id, course, grade, i_id in line_values(file, 4, "\t"):
                if s_id in self._students.keys():
                    self._students[s_id].add_grade(course, grade)
                if i_id in self._instructors.keys():
                    self._instructors[i_id].increment_student_count(course)
        except FileNotFoundError:
            print("Error: Grades file {} was not found.".format(file))

    def load_majors(self, file):
        '''Load the major definitions (required and elective courses) and process them.'''
        try:
            for major, course_type, course in line_values(file, 3, "\t"):
                for s in self._students.keys():
                    if course_type == 'R' and self._students[s]._major == major:
                        self._students[s].add_required_course(course)
                    if course_type == 'E' and self._students[s]._major == major:
                        self._students[s].add_elective_course(course)
                if major not in self._majors.keys():
                    self._majors[major] = Major(major)
                self._majors[major].add_course(course, course_type)
        except FileNotFoundError:
            print("Error: Majors file {} was not found.".format(file))

    def load_from_path(self, path):
        '''Read the data files from the specified path into the objects/structures'''
        self.load_students(os.path.join(path, "students.txt"))
        self.load_instructors(os.path.join(path, "instructors.txt"))
        self.load_grades(os.path.join(path, "grades.txt"))
        self.load_majors(os.path.join(path, "majors.txt"))

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

def validate_arguments():
    '''Validate the command line arguments.'''
    if len(sys.argv) > 2:
        # Invalid syntax - provide correct syntax and exit.
        print("Invalid syntax.")
        print("python Repository.py [path to data files]")
        quit()

    # Default to current working directory unless the user provides another directory.
    path = os.getcwd()
    if len(sys.argv) == 2:
        path = sys.argv[1]
    return path

if __name__ == '__main__':
    # Load the repository data.
    repo = Repository(validate_arguments())

    # Print the Majors, Students and Instructors in PrettyTables.
    print(repo.print_majors())
    print(repo.print_students())
    print(repo.print_instructors())
