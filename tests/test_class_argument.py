import unittest
from jnius.reflect import autoclass

class BasicsTest(unittest.TestCase):

    def test_static_methods(self):
        ClassArgument = autoclass('org.jnius.ClassArgument')
        self.assertEquals(ClassArgument.getName(ClassArgument), 'class org.jnius.ClassArgument')
