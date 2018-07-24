"""Homework 09
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 07/22/2018"""

import unittest
from unittest import TestCase
from Student import Student
from Instructor import Instructor
from Repository import Repository

# ----------
# UNIT TESTS
# ----------
class TestSystem(TestCase):
    '''Perform Unit Tests for the course tracking system'''

    def test_student(self):
        '''Test the Student class'''
        s1 = Student()
        self.assertEqual(s1._cwid, '')
        self.assertEqual(s1._name, '')
        self.assertEqual(s1._major, '')
        self.assertEqual(s1._grades, {})
        self.assertEqual(s1.prettyprint(), ['', '', []])
        s2 = Student('123456', 'Joseph, Joe', 'MSEE')
        s2.add_grade('SSW-540','A')
        s2.add_grade('SSW-555','B')
        self.assertEqual(s2._cwid, '123456')
        self.assertEqual(s2._name, 'Joseph, Joe')
        self.assertEqual(s2._major, 'MSEE')
        self.assertEqual(s2._grades, {'SSW-540':'A', 'SSW-555':'B'})
        self.assertEqual(s2.prettyprint(), ['123456', 'Joseph, Joe', ['SSW-540','SSW-555']])
    
    def test_instructor(self):
        '''Test the Instructor class'''
        i1 = Instructor()
        self.assertEqual(i1._cwid, '')
        self.assertEqual(i1._name, '')
        self.assertEqual(i1._department, '')
        self.assertEqual(i1._courses, {})
        i2 = Instructor('123456', 'Martin, Marty', 'MATH')
        i2.increment_student_count('SSW-540')
        i2.increment_student_count('SSW-555')
        i2.increment_student_count('SSW-555')
        self.assertEqual(i2._cwid, '123456')
        self.assertEqual(i2._name, 'Martin, Marty')
        self.assertEqual(i2._department, 'MATH')
        self.assertEqual(i2._courses, {'SSW-540':1, 'SSW-555':2})

    def test_repository(self):
        '''Test the Repository class'''
        repo = Repository()
        self.assertEqual(repo._instructors, {})
        self.assertEqual(repo._students, {})
        repo.load_students("test\\students.txt")
        self.assertEqual(repo._students['10103']._name,'Baldwin, C')
        self.assertEqual(repo._students['10103']._major, 'SFEN')
        self.assertEqual(repo._students['10103']._grades, {})
        self.assertEqual(repo._students['10115']._name, 'Wyatt, X')
        self.assertEqual(repo._students['10115']._major, 'SFEN')
        self.assertEqual(repo._students['10115']._grades, {})
        repo.load_instructors("test\\instructors.txt")
        self.assertEqual(repo._instructors['98765']._name, "Einstein, A")
        self.assertEqual(repo._instructors['98765']._department, "SFEN")
        self.assertEqual(repo._instructors['98765']._courses, {})
        self.assertEqual(repo._instructors['98764']._name, "Feynman, R")
        self.assertEqual(repo._instructors['98764']._department, "SFEN")
        self.assertEqual(repo._instructors['98764']._courses, {})
        repo.load_grades("test\\grades.txt")
        self.assertEqual(repo._students['10103']._grades, {'SSW 555':'A-', 'SSW 567':'A'})
        self.assertEqual(repo._students['10115']._grades, {'CPE 555':'A', 'SSW 567':'A'})
        self.assertEqual(repo._instructors['98765']._courses, {'SSW 567':2})
        self.assertEqual(repo._instructors['98764']._courses, {'CPE 555':1, 'SSW 555':1})

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
