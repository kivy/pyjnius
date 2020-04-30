# -*- coding: utf-8 -*-
# from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
from jnius.reflect import autoclass


try:
    long
except NameError:
    # Python 3
    long = int


def py2_encode(uni):
    if sys.version_info < (3, 0):
        uni = uni.encode('utf-8')
    return uni


class CharsAndStringsTest(unittest.TestCase):

    def test_char_fields(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testChar1, py2_encode('a'))
        if sys.version_info.major >= 3:
            self.assertEqual(test.testChar2, 'ä')
            self.assertEqual(test.testChar3, '☺')

        self.assertEqual(Test.testStaticChar1, py2_encode('a'))
        if sys.version_info.major >= 3:
            self.assertEqual(Test.testStaticChar2, 'ä')
            self.assertEqual(Test.testStaticChar3, '☺')

    def test_string_fields(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testString1, py2_encode("hello world"))
        if sys.version_info.major >= 3:
            self.assertEqual(test.testString2, "umlauts: äöü")
            self.assertEqual(test.testString3, "happy face: ☺")

        self.assertEqual(Test.testStaticString1, py2_encode("hello world"))
        if sys.version_info.major >= 3:
            self.assertEqual(Test.testStaticString2, "umlauts: äöü")
            self.assertEqual(Test.testStaticString3, "happy face: ☺")

    def test_char_methods(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testChar(1, py2_encode('a')), py2_encode('a'))
        if sys.version_info.major >= 3:
            self.assertEqual(test.testChar(2, 'ä'), 'ä')
            self.assertEqual(test.testChar(3, '☺'), '☺')

        self.assertEqual(Test.testStaticChar(1, py2_encode('a')), py2_encode('a'))
        if sys.version_info.major >= 3:
            self.assertEqual(Test.testStaticChar(2, 'ä'), 'ä')
            self.assertEqual(Test.testStaticChar(3, '☺'), '☺')

    def test_string_methods(self):
        Test = autoclass('org.jnius.CharsAndStrings',
                         include_protected=False, include_private=False)
        test = Test()

        self.assertEqual(test.testString(1, py2_encode("hello world")), py2_encode("hello world"))
        if sys.version_info.major >= 3:
            self.assertEqual(test.testString(2, "umlauts: äöü"), "umlauts: äöü")
            self.assertEqual(test.testString(3, "happy face: ☺"), "happy face: ☺")

        self.assertEqual(Test.testStaticString(1, py2_encode("hello world")), py2_encode("hello world"))
        if sys.version_info.major >= 3:
            self.assertEqual(Test.testStaticString(2, "umlauts: äöü"), "umlauts: äöü")
            self.assertEqual(Test.testStaticString(3, "happy face: ☺"), "happy face: ☺")
