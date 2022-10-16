from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
import jnius_config
from jnius import JavaMultipleMethod, JavaException
from jnius.reflect import autoclass


class VisibilityPublicProtectedTest(unittest.TestCase):

    def test_static_fields_public_protected(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, "StaticPublic")
        self.assertEqual(Test.fieldStaticPackageProtected, "StaticPackageProtected")
        self.assertEqual(Test.fieldStaticProtected, "StaticProtected")

    def test_child_static_fields_public_protected(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, "StaticPublic")
        self.assertEqual(Test.fieldStaticPackageProtected, "StaticPackageProtected")
        self.assertEqual(Test.fieldStaticProtected, "StaticProtected")

        self.assertTrue(hasattr(Test, 'fieldChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticPrivate'))

        self.assertEqual(Test.fieldChildStaticPublic, "ChildStaticPublic")
        self.assertEqual(Test.fieldChildStaticPackageProtected, "ChildStaticPackageProtected")
        self.assertEqual(Test.fieldChildStaticProtected, "ChildStaticProtected")

    def test_static_methods_public_protected(self):
        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), "StaticPublic")
        self.assertEqual(Test.methodStaticPackageProtected(), "StaticPackageProtected")
        self.assertEqual(Test.methodStaticProtected(), "StaticProtected")

    def test_child_static_methods_public_protected(self):
        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), "StaticPublic")
        self.assertEqual(Test.methodStaticPackageProtected(), "StaticPackageProtected")
        self.assertEqual(Test.methodStaticProtected(), "StaticProtected")

        self.assertTrue(hasattr(Test, 'methodChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodChildStaticPrivate'))

        self.assertEqual(Test.methodChildStaticPublic(), "ChildStaticPublic")
        self.assertEqual(Test.methodChildStaticPackageProtected(), "ChildStaticPackageProtected")
        self.assertEqual(Test.methodChildStaticProtected(), "ChildStaticProtected")

    def test_fields_public_protected(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, "Public")
        self.assertEqual(test.fieldPackageProtected, "PackageProtected")
        self.assertEqual(test.fieldProtected, "Protected")

    def test_child_fields_public_protected(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertTrue(hasattr(test, 'fieldPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, "Public")
        self.assertEqual(test.fieldPackageProtected, "PackageProtected")
        self.assertEqual(test.fieldProtected, "Protected")

        self.assertTrue(hasattr(test, 'fieldChildPublic'))
        self.assertTrue(hasattr(test, 'fieldChildPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldChildProtected'))
        self.assertFalse(hasattr(test, 'fieldChildPrivate'))

        self.assertEqual(test.fieldChildPublic, "ChildPublic")
        self.assertEqual(test.fieldChildPackageProtected, "ChildPackageProtected")
        self.assertEqual(test.fieldChildProtected, "ChildProtected")

    def test_methods_public_protected(self):

        Test = autoclass('org.jnius.VisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodPackageProtected'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), "Public")
        self.assertEqual(test.methodPackageProtected(), "PackageProtected")
        self.assertEqual(test.methodProtected(), "Protected")

    def test_child_methods_public_protected(self):

        Test = autoclass('org.jnius.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertTrue(hasattr(test, 'methodPackageProtected'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), "Public")
        self.assertEqual(test.methodPackageProtected(), "PackageProtected")
        self.assertEqual(test.methodProtected(), "Protected")

        self.assertTrue(hasattr(test, 'methodChildPublic'))
        self.assertTrue(hasattr(test, 'methodChildPackageProtected'))
        self.assertTrue(hasattr(test, 'methodChildProtected'))
        self.assertFalse(hasattr(test, 'methodChildPrivate'))

        self.assertEqual(test.methodChildPublic(), "ChildPublic")
        self.assertEqual(test.methodChildPackageProtected(), "ChildPackageProtected")
        self.assertEqual(test.methodChildProtected(), "ChildProtected")

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
