from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius import autoclass

class OutputArgs(unittest.TestCase):

    def test_string_output_args(self):
        String = autoclass('java.lang.String')
        string = String('word'.encode('utf-8'))
        btarray= [0] * 4
        string.getBytes(0, 4, btarray, 0)
        self.assertEqual(btarray, [119, 111, 114, 100])
