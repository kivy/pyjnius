from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass

class DirTest(unittest.TestCase):

    def test_varargs_dir(self):
        cls = autoclass("java.lang.System")
        assert isinstance(dir(cls.out.printf), list)
        #[(['java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream'),
        # (['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream')]
        for f in dir(cls.out.printf):
            assert isinstance(f, tuple)

    def test_array_dir(self):
        cls = autoclass("java.util.List")
        assert isinstance(dir(cls.toArray), list)
        #[([], 'java/lang/Object[]'),
        # (['java/lang/Object[]'], 'java/lang/Object[]')]
        for f in dir(cls.toArray):
            assert isinstance(f, tuple)

    def test_dir(self):
        cls = autoclass("java.lang.String")
        assert isinstance(dir(cls.valueOf), list)
        # [(['boolean'], 'java/lang/String'),
        #  (['char'], 'java/lang/String'),
        #  (['char[]'], 'java/lang/String'),
        #  (['char[]', 'int', 'int'], 'java/lang/String'),
        #  (['double'], 'java/lang/String'),
        #  (['float'], 'java/lang/String'),
        #  (['int'], 'java/lang/String'),
        #  (['java/lang/Object'], 'java/lang/String'),
        #  (['long'], 'java/lang/String')]
        for f in dir(cls.charAt):
            assert isinstance(f, tuple)





