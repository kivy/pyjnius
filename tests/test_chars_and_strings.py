# -*- coding: utf-8 -*-
# from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass, JavaException


class CharsAndStringsTest(unittest.TestCase):

    def test_char_fields(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testChar1, 'a')
        self.assertEqual(test.testChar2, 'ä')
        self.assertEqual(test.testChar3, '☺')

        self.assertEqual(Test.testStaticChar1, 'a')
        self.assertEqual(Test.testStaticChar2, 'ä')
        self.assertEqual(Test.testStaticChar3, '☺')

    def test_string_fields(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testString1, "hello world")
        self.assertEqual(test.testString2, "umlauts: äöü")
        self.assertEqual(test.testString3, "happy face: ☺")

        self.assertEqual(Test.testStaticString1, "hello world")
        self.assertEqual(Test.testStaticString2, "umlauts: äöü")
        self.assertEqual(Test.testStaticString3, "happy face: ☺")

    def test_char_methods(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testChar(1, 'a'), 'a')
        self.assertEqual(test.testChar(2, 'ä'), 'ä')
        self.assertEqual(test.testChar(3, '☺'), '☺')

        self.assertEqual(Test.testStaticChar(1, 'a'), 'a')
        self.assertEqual(Test.testStaticChar(2, 'ä'), 'ä')
        self.assertEqual(Test.testStaticChar(3, '☺'), '☺')

    def test_string_methods(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testString(1, "hello world"), "hello world")
        self.assertEqual(test.testString(2, "umlauts: äöü"), "umlauts: äöü")
        self.assertEqual(test.testString(3, "happy face: ☺"), "happy face: ☺")

        self.assertEqual(Test.testStaticString(1, "hello world"), "hello world")
        self.assertEqual(Test.testStaticString(2, "umlauts: äöü"), "umlauts: äöü")
        self.assertEqual(Test.testStaticString(3, "happy face: ☺"), "happy face: ☺")

    def test_char_array(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        charArray1 = ['a', 'b', 'c']
        charArray2 = ['a', 'ä', '☺']

        for c1, c2 in zip(charArray1, test.testCharArray1):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray1, test.testCharArray(1)):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray2, test.testCharArray2):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray2, test.testCharArray(2)):
            self.assertEqual(c1, c2)

    def test_static_char_array(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)

        charArray1 = ['a', 'b', 'c']
        charArray2 = ['a', 'ä', '☺']

        for c1, c2 in zip(charArray1, Test.testStaticCharArray1):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray1, Test.testStaticCharArray(1)):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray2, Test.testStaticCharArray2):
            self.assertEqual(c1, c2)
        for c1, c2 in zip(charArray2, Test.testStaticCharArray(2)):
            self.assertEqual(c1, c2)


    def test_java_string(self):
        JString = autoclass('java.lang.String')

        testString1 = JString('hello world')
        self.assertTrue(testString1.equals('hello world'))
        testString2 = JString('umlauts: äöü')
        self.assertTrue(testString2.equals('umlauts: äöü'))
        testString3 = JString('happy face: ☺')
        self.assertTrue(testString3.equals('happy face: ☺'))

    # two methods below are concerned with type-checking of arguments

    def test_pass_intfloat_as_string(self):
        CharsAndStrings = autoclass("org.jnius.CharsAndStrings")
        self.assertIsNone(CharsAndStrings.testStringDefNull)
        with self.assertRaisesRegex(TypeError, "Invalid instance of 'java/lang/Integer' passed for a 'java/lang/String'"):
            # we cannot provide an int to a String
            CharsAndStrings.setString("a", 2)
        with self.assertRaisesRegex(TypeError, "Invalid instance of 'java/lang/Float' passed for a 'java/lang/String'"):
            # we cannot provide an float to a String
            CharsAndStrings.setString("a", 2.2)
        alist = autoclass("java.util.ArrayList")()
        with self.assertRaisesRegex(TypeError, "Invalid instance of 'java/util/ArrayList' passed for a 'java/lang/String'"):
            # we cannot provide a list to a String
            CharsAndStrings.setString("a", alist)
        system = autoclass("java.lang.System")
        with self.assertRaises(JavaException):
            system.setErr("a string")

    def test_pass_string_as_int(self):
        CharsAndStrings = autoclass("org.jnius.CharsAndStrings")
        self.assertEqual(0, CharsAndStrings.testInt)
        with self.assertRaisesRegex(TypeError, "an integer is required"):
            # we cannot provide a String to an int
            CharsAndStrings.setInt("a", "2")
