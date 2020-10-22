'''
Test calling non-static methods on classes.
'''

from __future__ import absolute_import
import unittest
from jnius import autoclass, JavaException, JavaMethod, JavaMultipleMethod


class TestStatic(unittest.TestCase):

    def test_method(self):
        '''
        Call a non-static JavaMethod on a class,
        should raise JavaException.
        '''

        String = autoclass('java.lang.String')
        self.assertIsInstance(String.replaceAll, JavaMethod)
        self.assertEqual(String('foo').replaceAll('foo', 'bar'), 'bar')
        with self.assertRaises(JavaException):
            String.replaceAll('foo', 'bar')

    def test_multiplemethod(self):
        '''
        Call a non-static JavaMultipleMethod on a class,
        should raise JavaException.
        '''

        String = autoclass('java.lang.String')
        self.assertIsInstance(String.toString, JavaMultipleMethod)
        self.assertEqual(String('baz').toString(), 'baz')
        with self.assertRaises(JavaException):
            String.toString()


if __name__ == '__main__':
    unittest.main()
