'''
Enum in Java returns itself when trying to get a value, e.g.:

    SimpleEnum.GOOD

is of class instance SimpleEnum.

`javap -s SimpleEnum.class`::

    public final class org.jnius.SimpleEnum ... {
        public static final org.jnius.SimpleEnum GOOD;
            descriptor: Lorg/jnius/SimpleEnum;  <-- this
            ...
'''

from __future__ import absolute_import

import unittest
from jnius.reflect import autoclass


class TestSimpleEnum(unittest.TestCase):
    '''
    Test simple enum from java-src/org/jnius/SimpleEnum.java file.
    '''

    def test_enum(self):
        '''
        Make sure Enum returns something.
        '''
        SimpleEnum = autoclass('org.jnius.SimpleEnum')
        self.assertTrue(SimpleEnum)

    def test_value(self):
        '''
        Test whether the enum values return proper types and strings.
        '''
        SimpleEnum = autoclass('org.jnius.SimpleEnum')

        values = [SimpleEnum.GOOD, SimpleEnum.BAD, SimpleEnum.UGLY]
        for val in values:
            self.assertTrue(val)
            self.assertIsInstance(val, SimpleEnum)
            self.assertEqual(
                type(val),
                type(SimpleEnum.valueOf(val.toString()))
            )

            # 'GOOD', 'BAD', 'UGLY' strings
            self.assertEqual(
                val.toString(),
                SimpleEnum.valueOf(val.toString()).toString()
            )

    def test_value_nested(self):
        '''
        Static enum constants can be read through an enum instance without
        calling JNI's GetObjectField on a static field (pyjnius#32).
        '''
        SimpleEnum = autoclass('org.jnius.SimpleEnum')
        self.assertEqual(SimpleEnum.UGLY.UGLY.UGLY.toString(), 'UGLY')


if __name__ == '__main__':
    unittest.main()
