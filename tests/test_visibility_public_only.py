from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
import jnius_config
from jnius import JavaMethod, JavaStaticMethod, JavaException
from jnius.reflect import autoclass


class VisibilityPublicOnlyTest(unittest.TestCase):

    def test_static_fields_public_only(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=False, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertFalse(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, "StaticPublic")

    def test_child_static_fields_public_only(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertFalse(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, "StaticPublic")

        self.assertTrue(hasattr(Test, 'fieldChildStaticPublic'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticPrivate'))

        self.assertEqual(Test.fieldChildStaticPublic, "ChildStaticPublic")

    def test_static_methods_public_only(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=False, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertFalse(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), "StaticPublic")

    def test_child_static_methods_public_only(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertFalse(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), "StaticPublic")

        self.assertTrue(hasattr(Test, 'methodChildStaticPublic'))
        self.assertFalse(hasattr(Test, 'methodChildStaticPackageProtected'))
        self.assertFalse(hasattr(Test, 'methodChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodChildStaticPrivate'))

        self.assertEqual(Test.methodChildStaticPublic(), "ChildStaticPublic")

    def test_fields_public_only(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=False, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertFalse(hasattr(test, 'fieldPackageProtected'))
        self.assertFalse(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, "Public")

    def test_child_fields_public_only(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertFalse(hasattr(test, 'fieldPackageProtected'))
        self.assertFalse(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, "Public")

        self.assertTrue(hasattr(test, 'fieldChildPublic'))
        self.assertFalse(hasattr(test, 'fieldChildPackageProtected'))
        self.assertFalse(hasattr(test, 'fieldChildProtected'))
        self.assertFalse(hasattr(test, 'fieldChildPrivate'))

        self.assertEqual(test.fieldChildPublic, "ChildPublic")

    def test_methods_public_only(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=False, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertFalse(hasattr(test, 'methodPackageProtected'))
        self.assertFalse(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), "Public")

    def test_child_methods_public_only(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertFalse(hasattr(test, 'methodPackageProtected'))
        self.assertFalse(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), "Public")

        self.assertTrue(hasattr(test, 'methodChildPublic'))
        self.assertFalse(hasattr(test, 'methodChildPackageProtected'))
        self.assertFalse(hasattr(test, 'methodChildProtected'))
        self.assertFalse(hasattr(test, 'methodChildPrivate'))

        self.assertEqual(test.methodChildPublic(), "ChildPublic")

    def test_static_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticMultiArgs'))
        self.assertTrue(isinstance(Test.methodStaticMultiArgs, JavaStaticMethod))

        self.assertTrue(Test.methodStaticMultiArgs(True))
        with self.assertRaises(JavaException):
            Test.methodStaticMultiArgs(True, False)
        with self.assertRaises(JavaException):
            Test.methodStaticMultiArgs(True, False, True)

    def test_multi_methods(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=False, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodMultiArgs'))
        self.assertTrue(isinstance(Test.methodMultiArgs, JavaMethod))

        self.assertTrue(test.methodMultiArgs(True))
        with self.assertRaises(JavaException):
            test.methodMultiArgs(True, False)
        with self.assertRaises(JavaException):
           test.methodMultiArgs(True, False, True)
