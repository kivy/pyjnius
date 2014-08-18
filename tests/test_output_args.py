import unittest
from jnius import autoclass

class OutputArgs(unittest.TestCase):

    def test_string_output_args(self):
        String = autoclass('java.lang.String')
        string = String('word'.encode('utf-8'))
        btarray = [0] * 4
        string.getBytes(0, 4, btarray, 0)
        self.assertEquals(btarray, [119, 111, 114, 100])
