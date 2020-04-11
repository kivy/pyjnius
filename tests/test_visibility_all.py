from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
import jnius_config
from jnius import JavaMultipleMethod
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
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=True)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, py2_encode("StaticPublic"))
        self.assertEqual(Test.fieldStaticProtected, py2_encode("StaticProtected"))
        self.assertEqual(Test.fieldStaticPrivate, py2_encode("StaticPrivate"))

    def test_child_static_fields_all(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, py2_encode("StaticPublic"))
        self.assertEqual(Test.fieldStaticProtected, py2_encode("StaticProtected"))
        self.assertEqual(Test.fieldStaticPrivate, py2_encode("StaticPrivate"))

        self.assertTrue(hasattr(Test, 'fieldChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticProtected'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticPrivate'))

        self.assertEqual(Test.fieldChildStaticPublic, py2_encode("ChildStaticPublic"))
        self.assertEqual(Test.fieldChildStaticProtected, py2_encode("ChildStaticProtected"))
        self.assertEqual(Test.fieldChildStaticPrivate, py2_encode("ChildStaticPrivate"))

    def test_static_methods_all(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=True)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), py2_encode("StaticPublic"))
        self.assertEqual(Test.methodStaticProtected(), py2_encode("StaticProtected"))
        self.assertEqual(Test.methodStaticPrivate(), py2_encode("StaticPrivate"))

    def test_child_static_methods_all(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), py2_encode("StaticPublic"))
        self.assertEqual(Test.methodStaticProtected(), py2_encode("StaticProtected"))
        self.assertEqual(Test.methodStaticPrivate(), py2_encode("StaticPrivate"))

        self.assertTrue(hasattr(Test, 'methodChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodChildStaticProtected'))
        self.assertTrue(hasattr(Test, 'methodChildStaticPrivate'))

        self.assertEqual(Test.methodChildStaticPublic(), py2_encode("ChildStaticPublic"))
        self.assertEqual(Test.methodChildStaticProtected(), py2_encode("ChildStaticProtected"))
        self.assertEqual(Test.methodChildStaticPrivate(), py2_encode("ChildStaticPrivate"))

    def test_fields_all(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=True)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertTrue(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, py2_encode("Public"))
        self.assertEqual(test.fieldProtected, py2_encode("Protected"))
        self.assertEqual(test.fieldPrivate, py2_encode("Private"))

    def test_child_fields_all(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertTrue(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, py2_encode("Public"))
        self.assertEqual(test.fieldProtected, py2_encode("Protected"))
        self.assertEqual(test.fieldPrivate, py2_encode("Private"))

        self.assertTrue(hasattr(test, 'fieldChildPublic'))
        self.assertTrue(hasattr(test, 'fieldChildProtected'))
        self.assertTrue(hasattr(test, 'fieldChildPrivate'))

        self.assertEqual(test.fieldChildPublic, py2_encode("ChildPublic"))
        self.assertEqual(test.fieldChildProtected, py2_encode("ChildProtected"))
        self.assertEqual(test.fieldChildPrivate, py2_encode("ChildPrivate"))

    def test_methods_all(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=True)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertTrue(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), py2_encode("Public"))
        self.assertEqual(test.methodProtected(), py2_encode("Protected"))
        self.assertEqual(test.methodPrivate(), py2_encode("Private"))

    def test_child_methods_all(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)
        test = Test()

        self.assertTrue(hasattr(test, 'methodChildPublic'))
        self.assertTrue(hasattr(test, 'methodChildProtected'))
        self.assertTrue(hasattr(test, 'methodChildPrivate'))

        self.assertEqual(test.methodChildPublic(), py2_encode("ChildPublic"))
        self.assertEqual(test.methodChildProtected(), py2_encode("ChildProtected"))
        self.assertEqual(test.methodChildPrivate(), py2_encode("ChildPrivate"))

    def test_static_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)

        self.assertTrue(hasattr(Test, 'methodStaticMultiArgs'))
        self.assertTrue(isinstance(Test.methodStaticMultiArgs, JavaMultipleMethod))

        self.assertTrue(Test.methodStaticMultiArgs(True))
        self.assertTrue(Test.methodStaticMultiArgs(True, False))
        self.assertTrue(Test.methodStaticMultiArgs(True, False, True))

    def test_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=True)
        test = Test()

        self.assertTrue(hasattr(test, 'methodMultiArgs'))
        self.assertTrue(isinstance(Test.methodMultiArgs, JavaMultipleMethod))

        self.assertTrue(test.methodMultiArgs(True))
        self.assertTrue(test.methodMultiArgs(True, False))
        self.assertTrue(test.methodMultiArgs(True, False, True))
