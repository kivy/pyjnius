from __future__ import absolute_import
import unittest
from jnius import autoclass, protocol_map

class ComparableTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ComparableTest, self).__init__(*args, **kwargs)
    
    def test_compare_integer(self):
        five = autoclass('java.lang.Integer')(5)
        six = autoclass('java.lang.Integer')(6)
        six_two = autoclass('java.lang.Integer')(6)
        self.assertTrue(five < six)
        self.assertTrue(six > five)
        self.assertTrue(six == six_two)
        self.assertTrue(five <= six)
        self.assertTrue(six >= five)
        self.assertTrue(six >= six_two)
        self.assertTrue(six <= six_two)

if __name__ == '__main__':
    unittest.main()