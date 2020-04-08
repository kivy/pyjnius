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


class VisibilityPublicOnlyTest(unittest.TestCase):

    def test_static_fields_public(self):
        PublicOnlyTest = autoclass('org.jnius.VisibilityTest', public_only=True)

        self.assertTrue(hasattr(PublicOnlyTest, 'fieldStaticPublic'))
        self.assertFalse(hasattr(PublicOnlyTest, 'fieldStaticProtected'))
        self.assertFalse(hasattr(PublicOnlyTest, 'fieldStaticPrivate'))

        self.assertEqual(PublicOnlyTest.fieldStaticPublic, py2_encode("StaticPublic"))

    def test_static_methods_public(self):
        PublicOnlyTest = autoclass('org.jnius.VisibilityTest', public_only=True)

        self.assertTrue(hasattr(PublicOnlyTest, 'methodStaticPublic'))
        self.assertFalse(hasattr(PublicOnlyTest, 'methodStaticProtected'))
        self.assertFalse(hasattr(PublicOnlyTest, 'methodStaticPrivate'))

        self.assertEqual(PublicOnlyTest.methodStaticPublic(), py2_encode("StaticPublic"))

    def test_fields_public(self):
        PublicOnlyTest = autoclass('org.jnius.VisibilityTest', public_only=True)
        public_only_test = PublicOnlyTest()

        self.assertTrue(hasattr(public_only_test, 'fieldPublic'))
        self.assertFalse(hasattr(public_only_test, 'fieldProtected'))
        self.assertFalse(hasattr(public_only_test, 'fieldPrivate'))

        self.assertEqual(public_only_test.fieldPublic, py2_encode("Public"))

    def test_methods_public(self):
        PublicOnlyTest = autoclass('org.jnius.VisibilityTest', public_only=True)
        public_only_test = PublicOnlyTest()

        self.assertTrue(hasattr(public_only_test, 'methodPublic'))
        self.assertFalse(hasattr(public_only_test, 'methodProtected'))
        self.assertFalse(hasattr(public_only_test, 'methodPrivate'))

        self.assertEqual(public_only_test.methodPublic(), py2_encode("Public"))
