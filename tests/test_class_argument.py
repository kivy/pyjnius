from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import unittest
from jnius.reflect import autoclass

class BasicsTest(unittest.TestCase):

    def test_static_methods(self):
        ClassArgument = autoclass('org.jnius.ClassArgument')
        self.assertEquals(ClassArgument.getName(ClassArgument), 'class org.jnius.ClassArgument')
