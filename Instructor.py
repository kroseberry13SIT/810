"""Homework 10
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 07/29/2018"""

from collections import defaultdict

# ----------
# Instructor Class: Represents an instructor of a college/university
# ----------

class Instructor:
    '''Encapsulates the Instructor data of a college/university.'''
    
    def __init__(self, cwid="", name="", department=""):
        '''Initialize a new Instructor instance.'''
        self._cwid = cwid
        self._name = name
        self._department = department
        self._courses = defaultdict(int)

    def increment_student_count(self, course):
        '''Increment the student count for the given course.'''
        self._courses[course] += 1

    def prettyprint(self):
        '''Build an array for each course suitable for printing in a PrettyTable.'''
        for c in sorted(self._courses.keys()):
            yield [self._cwid, self._name, self._department, c, self._courses[c]]
        