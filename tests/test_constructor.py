'''
Test creating an instance of a Java class and fetching its values.
'''

from __future__ import absolute_import
import unittest
from jnius import autoclass, JavaException


class TestConstructor(unittest.TestCase):
    '''
    TestCase for using constructors with PyJNIus.
    '''

    def test_constructor_none(self):
        '''
        Empty constructor, baked value in the .java file.
        '''

        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        inst = ConstructorTest()
        self.assertEqual(inst.ret, 753)
        self.assertTrue(ConstructorTest._class.isInstance(inst))
        self.assertTrue(inst.getClass().isInstance(inst))

    def test_constructor_int(self):
        '''
        Constructor expecting int and setting it as public 'ret' property.
        '''

        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        inst = ConstructorTest(123)
        self.assertEqual(inst.ret, 123)
        self.assertTrue(ConstructorTest._class.isInstance(inst))
        self.assertTrue(inst.getClass().isInstance(inst))

    def test_constructor_string(self):
        '''
        Constructor expecting char, casting it to int and setting it
        as public 'ret' property.
        '''

        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        inst = ConstructorTest('a')
        self.assertEqual(inst.ret, ord('a'))
        self.assertTrue(ConstructorTest._class.isInstance(inst))
        self.assertTrue(inst.getClass().isInstance(inst))

    def test_constructor_multiobj(self):
        '''
        Constructor expecting String.
        '''

        outputStream = autoclass('java.lang.System').out
        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        inst = ConstructorTest(outputStream, signature="(Ljava/io/OutputStream;)V")
        self.assertEqual(inst.ret, 42)
        self.assertTrue(ConstructorTest._class.isInstance(inst))
        self.assertTrue(inst.getClass().isInstance(inst))

    def test_constructor_int_string(self):
        '''
        Constructor expecting int and char, casting char to int and summing it
        as public 'ret' property.
        '''

        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        inst = ConstructorTest(3, 'a')
        self.assertEqual(inst.ret, 3 + ord('a'))
        self.assertTrue(ConstructorTest._class.isInstance(inst))
        self.assertTrue(inst.getClass().isInstance(inst))

    def test_constructor_exception(self):
        '''
        No such constructor found (no such signature),
        should raise JavaException.
        '''

        ConstructorTest = autoclass('org.jnius.ConstructorTest')
        with self.assertRaises(JavaException):
            ConstructorTest('1.', 2.0, False)


if __name__ == '__main__':
    unittest.main()
