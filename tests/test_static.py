'''
Test calling non-static methods on classes.
'''

import unittest
from jnius import (autoclass, JavaClass, JavaException, JavaField, JavaMethod,
                   JavaMultipleMethod, MetaJavaClass)


class TestStatic(unittest.TestCase):

    def test_manual_static_field(self):
        class System(JavaClass, metaclass=MetaJavaClass):
            __javaclass__ = 'java/lang/System'
            out = JavaField('Ljava/io/PrintStream;', static=True)

        self.assertEqual(System.out.getClass().getName(), 'java.io.PrintStream')

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
