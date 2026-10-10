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

    def test_cast_to_abstract_class(self):
        stream = autoclass('java.lang.System').out
        output_stream = cast('java.io.OutputStream', stream)

        self.assertEqual(output_stream.__javaclass__, 'java/io/OutputStream')
        self.assertEqual(output_stream.getClass().getName(), 'java.io.PrintStream')
