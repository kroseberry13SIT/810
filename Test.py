"""Homework 11
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 08/05/2018"""

import unittest
from unittest import TestCase
from Student import Student
from Instructor import Instructor
from Repository import Repository
from Major import Major

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
        self.assertFalse(s1._elective_taken)
        self.assertEqual(s1._remaining_required, set())
        self.assertEqual(s1._remaining_electives, set())
        s2 = Student('123456', 'Joseph, Joe', 'MSEE')
        s2.add_grade('SSW-540','A')
        s2.add_grade('SSW-555','B')
        s2.add_grade('SSW-555','B+')
        s2.add_grade('SSW-567','F')
        s2.add_required_course('SSW-540')
        s2.add_required_course('SSW-567')
        s2.add_required_course('SSW-990')
        s2.add_elective_course('SSW-555')
        s2.add_elective_course('SSW-999')
        self.assertEqual(s2._cwid, '123456')
        self.assertEqual(s2._name, 'Joseph, Joe')
        self.assertEqual(s2._major, 'MSEE')
        self.assertEqual(s2._grades, {'SSW-540':'A', 'SSW-555':'B+', 'SSW-567':'F'})
        self.assertEqual(s2._remaining_required, set(['SSW-567','SSW-990']))
        self.assertEqual(s2._remaining_electives, set(['SSW-999']))
    
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

    def test_major(self):
        '''Test the Major class'''
        m1 = Major('SFEN')
        self.assertEqual(m1._id, 'SFEN')
        self.assertEqual(m1._required, set())
        self.assertEqual(m1._electives, set())
        m1.add_course('SSW-540','R')
        m1.add_course('SSW-810','E')
        m1.add_course('SSW-999','X')
        self.assertEqual(m1._required, set(['SSW-540']))
        self.assertEqual(m1._electives, set(['SSW-810']))

    def test_repository(self):
        '''Test the Repository class'''
        repo = Repository(".\\test")
        self.assertEqual(repo._students['10103']._name,'Baldwin, C')
        self.assertEqual(repo._students['10103']._major, 'SFEN')
        self.assertEqual(repo._students['10115']._name, 'Wyatt, X')
        self.assertEqual(repo._students['10115']._major, 'SFEN')
        self.assertEqual(repo._instructors['98765']._name, "Einstein, A")
        self.assertEqual(repo._instructors['98765']._department, "SFEN")
        self.assertEqual(repo._instructors['98764']._name, "Feynman, R")
        self.assertEqual(repo._instructors['98764']._department, "SFEN")
        self.assertEqual(repo._students['10103']._grades, {'SSW 564':'A-', 'SSW 567':'A', 'SSW 687':'B'})
        self.assertEqual(repo._students['10115']._grades, {'SSW 564':'B+', 'SSW 567':'A', 'SSW 687':'A'})
        self.assertEqual(repo._instructors['98765']._courses, {'SSW 540':3, 'SSW 567':4})
        self.assertEqual(repo._instructors['98764']._courses, {'SSW 564':3, 'SSW 687':3})
        self.assertEqual(repo._majors['SFEN']._required, set(['SSW 540','SSW 555','SSW 564','SSW 567']))
        self.assertEqual(repo._majors['SFEN']._electives, set(['SSW 533','SSW 565','SSW 690','SSW 695']))
        self.assertEqual(repo._students['10103']._remaining_required, set(['SSW 540','SSW 555']))
        self.assertEqual(repo._students['10103']._remaining_electives, set(['SSW 533','SSW 565','SSW 690','SSW 695']))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
