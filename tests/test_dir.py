from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass

class DirTest(unittest.TestCase):

    def test_varargs_dir(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.lang.System')
        # >>> dir(cls.out.printf)
        # [(['java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream'),
        # (['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream')]

        cls = autoclass("java.lang.System")
        result = dir(cls.out.printf)

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert (['java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream') in result
        assert (['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream') in result

    def test_array_dir(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.util.List')
        # >>> dir(cls.toArray)
        # [([], 'java/lang/Object[]'),
        # (['java/lang/Object[]'], 'java/lang/Object[]')]

        cls = autoclass("java.util.List")
        result = dir(cls.toArray)

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert ([], 'java/lang/Object[]') in result
        assert (['java/lang/Object[]'], 'java/lang/Object[]') in result

    def test_dir(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.lang.String')
        # >>> dir(cls.valueOf)
        # [(['boolean'], 'java/lang/String'),
        #  (['char'], 'java/lang/String'),
        #  (['char[]'], 'java/lang/String'),
        #  (['char[]', 'int', 'int'], 'java/lang/String'),
        #  (['double'], 'java/lang/String'),
        #  (['float'], 'java/lang/String'),
        #  (['int'], 'java/lang/String'),
        #  (['java/lang/Object'], 'java/lang/String'),
        #  (['long'], 'java/lang/String')]

        cls = autoclass("java.lang.String")
        result = dir(cls.valueOf)

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert result == [
            (['boolean'], 'java/lang/String'),
            (['char'], 'java/lang/String'),
            (['char[]'], 'java/lang/String'),
            (['char[]', 'int', 'int'], 'java/lang/String'),
            (['double'], 'java/lang/String'),
            (['float'], 'java/lang/String'),
            (['int'], 'java/lang/String'),
            (['java/lang/Object'], 'java/lang/String'),
            (['long'], 'java/lang/String')
        ]
