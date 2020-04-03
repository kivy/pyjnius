from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius import autoclass

class StringArgumentForByteArrayTest(unittest.TestCase):

    def test_string_arg_for_byte_array(self):
        # the ByteBuffer.wrap() accept only byte[].
        ByteBuffer = autoclass('java.nio.ByteBuffer')
        self.assertIsNotNone(ByteBuffer.wrap(b'hello world'))

    def test_string_arg_with_signed_char(self):
        ByteBuffer = autoclass('java.nio.ByteBuffer')
        self.assertIsNotNone(ByteBuffer.wrap(b'\x00\xffHello World\x7f'))

    def test_fill_byte_array(self):
        arr = [0, 0, 0]
        Test = autoclass('org.jnius.BasicsTest')()
        Test.fillByteArray(arr)
        # we don't received signed byte, but unsigned in python.
        self.assertEqual(
            arr,
            [127, 1, 129])

    def test_create_bytearray(self):
        StringBufferInputStream = autoclass('java.io.StringBufferInputStream')
        nis = StringBufferInputStream("Hello world")
        barr = bytearray("\x00" * 5, encoding="utf8")
        self.assertEqual(nis.read(barr, 0, 5), 5)
        self.assertEqual(barr, b"Hello")

    def test_bytearray_ascii(self):
        ByteArrayInputStream = autoclass('java.io.ByteArrayInputStream')
        s = b"".join(bytes(x) for x in range(256))
        nis = ByteArrayInputStream(s)
        barr = bytearray("\x00" * 256, encoding="ascii")
        self.assertEqual(nis.read(barr, 0, 256), 256)
        self.assertEqual(barr[:256], s[:256])

    def test_empty_bytearray(self):
        Test = autoclass('org.jnius.BasicsTest')()
        arr = Test.methodReturnEmptyByteArray()
        self.assertEqual(len(arr), 0)
        with self.assertRaises(IndexError):
            arr[0]
        self.assertEqual(arr, [])
        self.assertEqual(arr[:1], [])
        self.assertEqual(arr.tostring(), b'')
