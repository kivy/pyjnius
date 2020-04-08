from __future__ import print_function
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


class VisibilityAllTest(unittest.TestCase):

    def test_static_fields_all(self):
        Test = autoclass('org.jnius.VisibilityTest')

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        # self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        # self.assertTrue(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, py2_encode("StaticPublic"))
        # self.assertEqual(Test.fieldStaticProtected, py2_encode("StaticProtected"))
        # self.assertEqual(Test.fieldStaticPrivate, py2_encode("StaticPrivate"))

    def test_static_methods_all(self):
        Test = autoclass('org.jnius.VisibilityTest')

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), py2_encode("StaticPublic"))
        self.assertEqual(Test.methodStaticProtected(), py2_encode("StaticProtected"))
        self.assertEqual(Test.methodStaticPrivate(), py2_encode("StaticPrivate"))

    def test_fields_all(self):
        Test = autoclass('org.jnius.VisibilityTest')
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        # self.assertTrue(hasattr(test, 'fieldProtected'))
        # self.assertTrue(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, py2_encode("Public"))
        # self.assertEqual(test.fieldProtected, py2_encode("Protected"))
        # self.assertEqual(test.fieldPrivate, py2_encode("Private"))

    def test_methods_all(self):
        Test = autoclass('org.jnius.VisibilityTest')
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertTrue(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), py2_encode("Public"))
        self.assertEqual(test.methodProtected(), py2_encode("Protected"))
        self.assertEqual(test.methodPrivate(), py2_encode("Private"))
