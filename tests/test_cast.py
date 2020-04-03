from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass
from jnius import cast


class MultipleSignatureTest(unittest.TestCase):
    def test_multiple_constructors(self):
        String = autoclass('java.lang.String')
        s = String('hello world')
        self.assertEqual(s.__javaclass__, 'java/lang/String')
        o = cast('java.lang.Object', s)
        self.assertEqual(o.__javaclass__, 'java/lang/Object')

    def test_mmap_toString(self):
        mapClass = autoclass('java.util.HashMap')
        hmap = mapClass()
        hmap.put("a", "1")
        hmap.toString()
        mmap = cast('java.util.Map', hmap)
        mmap.toString()
        mmap.getClass()
