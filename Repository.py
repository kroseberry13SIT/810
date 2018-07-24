"""Homework 09
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 07/22/2018"""

# ----------
# Repository Class: Storage of all data for the Course Tracker System
# ----------

import os
import sys

from Student import Student
from Instructor import Instructor
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
        if path != "":
            self.load_from_path(path)

    def load_students(self, file):
        '''Load the students data from the specified file.'''
        try:
            for s in line_values(file, 3, "\t"):
                self._students[s[0]] = Student(s[0], s[1], s[2])
        except FileNotFoundError:
            print("Error: Students file {} was not found.".format(file))

    def load_instructors(self, file):
        '''Load the instructors data from the specified file.'''
        try:
            for i in line_values(file, 3, "\t"):
                self._instructors[i[0]] = Instructor(i[0], i[1], i[2])
        except FileNotFoundError:
            print("Error: Instructors file {} was not found.".format(file))

    def load_grades(self, file):
        '''Load the grades data from the specified file and process them.'''
        try:
            for g in line_values(file, 4, "\t"):
                if g[0] in self._students.keys():
                    self._students[g[0]].add_grade(g[1],g[2])
                if g[3] in self._instructors.keys():
                    self._instructors[g[3]].increment_student_count(g[1])
        except FileNotFoundError:
            print("Error: Grades file {} was not found.".format(file))

    def load_from_path(self, path):
        '''Read the data files from the specified path into the objects/structures'''
        self.load_students(os.path.join(path, "students.txt"))
        self.load_instructors(os.path.join(path, "instructors.txt"))
        self.load_grades(os.path.join(path, "grades.txt"))

    def print_students(self):
        pt = PrettyTable(field_names=['CWID','Name','Completed Courses'])
        for s in self._students.keys():
            pt.add_row(self._students[s].prettyprint())
        return pt

    def print_instructors(self):
        pt = PrettyTable(field_names=['CWID','Name','Dept','Course','Students'])
        for i in self._instructors.keys():
            for pp in self._instructors[i].prettyprint():
                pt.add_row(pp)
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

    # Print the Students and Instructors in PrettyTables.
    print(repo.print_students())
    print(repo.print_instructors())
