"""Homework 11
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 08/05/2018"""

from collections import defaultdict

# ----------
# Student Class: Represents a student of a college/university
# ----------

class Student:
    ''' Encapsulates the Student data for a college/university.'''
    
    __valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
    
    def __init__(self, cwid="", name="", major=""):
        '''Initialize a new Student instance.'''
        self._cwid = cwid
        self._name = name
        self._major = major
        self._elective_taken = False
        self._grades = defaultdict(str)
        self._remaining_required = set()
        self._remaining_electives = set()

    def add_grade(self, course, grade):
        '''Add a grade for a given course.'''
        self._grades[course] = grade

    def _add_course(self, course, courses):
        '''Add the course only if the student has not  yet taken and passed it.
           Return True if the student passed, False if failed.'''
        passed = False
        if course in self._grades.keys() and self._grades[course] in Student.__valid_grades:
            passed = True
        else:
            courses.add(course)
        return passed

    def add_required_course(self, course):
        '''Add a required course only if the student has not yet taken and passed it.'''
        self._add_course(course, self._remaining_required)

    def add_elective_course(self, course):
        '''Add an elective course only if the student has not yet taken and passed it.'''
        if self._add_course(course, self._remaining_electives):
            self._elective_taken = True

    def prettyprint(self):
        '''Provide an array suitable for printing in a PrettyTable.'''
        electives = sorted(self._remaining_electives)
        if self._elective_taken:
            electives = None
        return [self._cwid, self._name, self._major, sorted(self._grades), \
                sorted(self._remaining_required), electives]
