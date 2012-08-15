import unittest
from jnius.reflect import autoclass

class MultipleSignature(unittest.TestCase):

    def test_multiple_constructors(self):
        String = autoclass('java.lang.String')
        self.assertIsNotNone(String('Hello World'))
        self.assertIsNotNone(String(list('Hello World')))
        self.assertIsNotNone(String(list('Hello World'), 3, 5))

    def test_multiple_methods(self):
        String = autoclass('java.lang.String')
        s = String('hello')
        self.assertEquals(s.getBytes(), [104, 101, 108, 108, 111])
        self.assertEquals(s.getBytes('utf8'), [104, 101, 108, 108, 111])
        self.assertEquals(s.indexOf(ord('e')), 1)
        self.assertEquals(s.indexOf(ord('e'), 2), -1)
