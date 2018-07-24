"""Homework 09
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 07/22/2018"""

from collections import defaultdict

# ----------
# Student Class: Represents a student of a college/university
# ----------

class Student:
    ''' Encapsulates the Student data for a college/university.'''
    
    def __init__(self, cwid="", name="", major=""):
        '''Initialize a new Student instance.'''
        self._cwid = cwid
        self._name = name
        self._major = major
        self._grades = defaultdict(str)

    def add_grade(self, course, grade):
        '''Add a grade for a given course.'''
        self._grades[course] = grade

    def prettyprint(self):
        '''Provide an array suitable for printing in a PrettyTable.'''
        return [self._cwid, self._name, sorted(self._grades)]
