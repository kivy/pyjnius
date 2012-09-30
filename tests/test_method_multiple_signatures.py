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

    def test_multiple_methods_no_args(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve(), 'resolved no args')

    def test_multiple_methods_one_arg(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve('arg'), 'resolved one arg')

    def test_multiple_methods_two_args(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve('one', 'two'), 'resolved two args')

    def test_multiple_methods_two_string_and_an_integer(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve('one', 'two', 1), 'resolved two string and an integer')

    def test_multiple_methods_two_string_and_two_integers(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve('one', 'two', 1, 2), 'resolved two string and two integers')

    def test_multiple_methods_varargs(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve(1, 2, 3), 'resolved varargs')

    def test_multiple_methods_two_args_and_varargs(self):
        MultipleMethods = autoclass('org.jnius.MultipleMethods')
        self.assertEqual(MultipleMethods.resolve('one', 'two', 1, 2, 3), 'resolved two args and varargs')
