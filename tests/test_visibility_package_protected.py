from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
import jnius_config
from jnius import JavaMethod, JavaStaticMethod, JavaException
from jnius.reflect import autoclass


class VisibilityPackageProtectedTest(unittest.TestCase):
    """This unittest verifies the correct visibility of package protected methods and fields.

    Observe that org.jnius2.ChildVisibilityTest is not in the same package as
    it's parent class. If `include_protected` is True and `include_private`
    is False, only the package protected methods and fields in the child class
    should be visible.
    """

    def test_child_static_fields_package_protected(self):
        Test = autoclass('org.jnius2.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'fieldStaticPublic'))
        self.assertFalse(hasattr(Test, 'fieldStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldStaticPrivate'))

        self.assertEqual(Test.fieldStaticPublic, "StaticPublic")
        self.assertEqual(Test.fieldStaticProtected, "StaticProtected")

        self.assertTrue(hasattr(Test, 'fieldChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'fieldChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'fieldChildStaticPrivate'))

        self.assertEqual(Test.fieldChildStaticPublic, "ChildStaticPublic")
        self.assertEqual(Test.fieldChildStaticPackageProtected, "ChildStaticPackageProtected")
        self.assertEqual(Test.fieldChildStaticProtected, "ChildStaticProtected")

    def test_child_static_methods_package_protected(self):
        Test = autoclass('org.jnius2.ChildVisibilityTest', include_protected=True, include_private=False)

        self.assertTrue(hasattr(Test, 'methodStaticPublic'))
        self.assertFalse(hasattr(Test, 'methodStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodStaticPrivate'))

        self.assertEqual(Test.methodStaticPublic(), "StaticPublic")
        self.assertEqual(Test.methodStaticProtected(), "StaticProtected")

        self.assertTrue(hasattr(Test, 'methodChildStaticPublic'))
        self.assertTrue(hasattr(Test, 'methodChildStaticPackageProtected'))
        self.assertTrue(hasattr(Test, 'methodChildStaticProtected'))
        self.assertFalse(hasattr(Test, 'methodChildStaticPrivate'))

        self.assertEqual(Test.methodChildStaticPublic(), "ChildStaticPublic")
        self.assertEqual(Test.methodChildStaticPackageProtected(), "ChildStaticPackageProtected")
        self.assertEqual(Test.methodChildStaticProtected(), "ChildStaticProtected")

    def test_child_fields_package_protected(self):

        Test = autoclass('org.jnius2.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'fieldPublic'))
        self.assertFalse(hasattr(test, 'fieldPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldProtected'))
        self.assertFalse(hasattr(test, 'fieldPrivate'))

        self.assertEqual(test.fieldPublic, "Public")
        self.assertEqual(test.fieldProtected, "Protected")

        self.assertTrue(hasattr(test, 'fieldChildPublic'))
        self.assertTrue(hasattr(test, 'fieldChildPackageProtected'))
        self.assertTrue(hasattr(test, 'fieldChildProtected'))
        self.assertFalse(hasattr(test, 'fieldChildPrivate'))

        self.assertEqual(test.fieldChildPublic, "ChildPublic")
        self.assertEqual(test.fieldChildPackageProtected, "ChildPackageProtected")
        self.assertEqual(test.fieldChildProtected, "ChildProtected")

    def test_child_methods_package_protected(self):

        Test = autoclass('org.jnius2.ChildVisibilityTest', include_protected=True, include_private=False)
        test = Test()

        self.assertTrue(hasattr(test, 'methodPublic'))
        self.assertFalse(hasattr(test, 'methodPackageProtected'))
        self.assertTrue(hasattr(test, 'methodProtected'))
        self.assertFalse(hasattr(test, 'methodPrivate'))

        self.assertEqual(test.methodPublic(), "Public")
        self.assertEqual(test.methodProtected(), "Protected")

        self.assertTrue(hasattr(test, 'methodChildPublic'))
        self.assertTrue(hasattr(test, 'methodChildPackageProtected'))
        self.assertTrue(hasattr(test, 'methodChildProtected'))
        self.assertFalse(hasattr(test, 'methodChildPrivate'))

        self.assertEqual(test.methodChildPublic(), "ChildPublic")
        self.assertEqual(test.methodChildPackageProtected(), "ChildPackageProtected")
        self.assertEqual(test.methodChildProtected(), "ChildProtected")
