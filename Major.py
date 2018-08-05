"""Homework 12
   Student: Keith M. Roseberry
   Class: SSW-810-WS
   Term: Summer, 2018
   Due Date: 08/12/2018"""

# ----------
# Major Class: Represents a major of study at a college/university
# ----------

class Major:
    ''' Encapsulates the Major data for a college/university.'''
    
    def __init__(self, id=""):
        '''Initialize a new Student instance.'''
        self._id = id
        self._required = set()
        self._electives = set()

    def add_course(self, course, course_type):
        '''Add the course to the appropriate set based on the type.'''
        if course_type == 'R':
            self._required.add(course)
        if course_type == 'E':
            self._electives.add(course)

    def prettyprint(self):
        '''Provide an array suitable for printing in a PrettyTable.'''
        return [self._id, sorted(self._required), sorted(self._electives)]
