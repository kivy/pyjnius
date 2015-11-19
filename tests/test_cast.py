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
        self.assertEquals(s.__javaclass__, 'java/lang/String')
        o = cast('java.lang.Object', s)
        self.assertEquals(o.__javaclass__, 'java/lang/Object')

