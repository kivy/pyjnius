from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
import jnius_config
from jnius import JavaMultipleMethod, JavaException
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


class VisibilityPublicProtectedTest(unittest.TestCase):

    def test_static_fields_public_protected(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, py2_encode("StaticPublic"))
        self.assertEqual(Test.fieldStaticPackageProtected, py2_encode("StaticPackageProtected"))
        self.assertEqual(Test.fieldStaticProtected, py2_encode("StaticProtected"))

    def test_child_static_fields_public_protected(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, py2_encode("StaticPublic"))
        self.assertEqual(Test.fieldStaticPackageProtected, py2_encode("StaticPackageProtected"))
        self.assertEqual(Test.fieldStaticProtected, py2_encode("StaticProtected"))

        self.assertTrue(hasattr(Test, 'fieldChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticPrivate'))

        self.assertEqual(Test.fieldChildStaticPublic, py2_encode("ChildStaticPublic"))
        self.assertEqual(Test.fieldChildStaticPackageProtected, py2_encode("ChildStaticPackageProtected"))
        self.assertEqual(Test.fieldChildStaticProtected, py2_encode("ChildStaticProtected"))

    def test_static_methods_public_protected(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), py2_encode("StaticPublic"))
        self.assertEqual(Test.methodStaticPackageProtected(), py2_encode("StaticPackageProtected"))
        self.assertEqual(Test.methodStaticProtected(), py2_encode("StaticProtected"))

    def test_child_static_methods_public_protected(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), py2_encode("StaticPublic"))
        self.assertEqual(Test.methodStaticPackageProtected(), py2_encode("StaticPackageProtected"))
        self.assertEqual(Test.methodStaticProtected(), py2_encode("StaticProtected"))

        self.assertTrue(hasattr(Test, 'methodChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodChildStaticPrivate'))

        self.assertEqual(Test.methodChildStaticPublic(), py2_encode("ChildStaticPublic"))
        self.assertEqual(Test.methodChildStaticPackageProtected(), py2_encode("ChildStaticPackageProtected"))
        self.assertEqual(Test.methodChildStaticProtected(), py2_encode("ChildStaticProtected"))

    def test_fields_public_protected(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, py2_encode("Public"))
        self.assertEqual(test.fieldPackageProtected, py2_encode("PackageProtected"))
        self.assertEqual(test.fieldProtected, py2_encode("Protected"))

    def test_child_fields_public_protected(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, py2_encode("Public"))
        self.assertEqual(test.fieldPackageProtected, py2_encode("PackageProtected"))
        self.assertEqual(test.fieldProtected, py2_encode("Protected"))

        self.assertTrue(hasattr(test, 'fieldChildPublic'))
        self.assertTrue(hasattr(test, 'fieldChildPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldChildProtected'))
        self.assertFalse(hasattr(test, 'fieldChildPrivate'))

        self.assertEqual(test.fieldChildPublic, py2_encode("ChildPublic"))
        self.assertEqual(test.fieldChildPackageProtected, py2_encode("ChildPackageProtected"))
        self.assertEqual(test.fieldChildProtected, py2_encode("ChildProtected"))

    def test_methods_public_protected(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodPackageProtected'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), py2_encode("Public"))
        self.assertEqual(test.methodPackageProtected(), py2_encode("PackageProtected"))
        self.assertEqual(test.methodProtected(), py2_encode("Protected"))

    def test_child_methods_public_protected(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodPackageProtected'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), py2_encode("Public"))
        self.assertEqual(test.methodPackageProtected(), py2_encode("PackageProtected"))
        self.assertEqual(test.methodProtected(), py2_encode("Protected"))

        self.assertTrue(hasattr(test, 'methodChildPublic'))
        self.assertTrue(hasattr(test, 'methodChildPackageProtected'))
        self.assertTrue(hasattr(test, 'methodChildProtected'))
        self.assertFalse(hasattr(test, 'methodChildPrivate'))

        self.assertEqual(test.methodChildPublic(), py2_encode("ChildPublic"))
        self.assertEqual(test.methodChildPackageProtected(), py2_encode("ChildPackageProtected"))
        self.assertEqual(test.methodChildProtected(), py2_encode("ChildProtected"))

    def test_static_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticMultiArgs'))
        self.assertTrue(isinstance(Test.methodStaticMultiArgs, JavaMultipleMethod))

        self.assertTrue(Test.methodStaticMultiArgs(True))
        self.assertTrue(Test.methodStaticMultiArgs(True, False))
        with self.assertRaises(JavaException):
            Test.methodStaticMultiArgs(True, False, True)

    def test_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodMultiArgs'))
        self.assertTrue(isinstance(Test.methodMultiArgs, JavaMultipleMethod))

        self.assertTrue(test.methodMultiArgs(True))
        self.assertTrue(test.methodMultiArgs(True, False))
        with self.assertRaises(JavaException):
           test.methodMultiArgs(True, False, True)
