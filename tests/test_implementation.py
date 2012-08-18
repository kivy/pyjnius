import unittest
from jnius.reflect import autoclass

class ImplementationTest(unittest.TestCase):

    def test_println(self):
        # System.out.println implies recursive lookup, and j_self assignation.
        # It was crashing during the implementation :/
        System = autoclass('java.lang.System')
        System.out.println('')
