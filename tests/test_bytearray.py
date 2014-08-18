import unittest
from jnius import autoclass


class StringArgumentForByteArrayTest(unittest.TestCase):

    def test_string_arg_for_byte_array(self):
        # the ByteBuffer.wrap() accept only byte[].
        ByteBuffer = autoclass('java.nio.ByteBuffer')
        self.assertIsNotNone(ByteBuffer.wrap('hello world'))
