from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass

class DirTest(unittest.TestCase):

    def test_varargs_signatures(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.lang.System')
        # >>> cls.out.printf.signatures()
        # [(['java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream'),
        # (['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream')]

        cls = autoclass("java.lang.System")
        result = cls.out.printf.signatures()

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert (['java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream') in result
        assert (['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/io/PrintStream') in result

    def test_array_signatures(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.util.List')
        # >>> cls.toArray.signatures()
        # [([], 'java/lang/Object[]'),
        # (['java/lang/Object[]'], 'java/lang/Object[]')]

        cls = autoclass("java.util.List")
        result = cls.toArray.signatures()

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert ([], 'java/lang/Object[]') in result
        assert (['java/lang/Object[]'], 'java/lang/Object[]') in result

    def test_signatures(self):
        # >>> from jnius import autoclass
        # >>> cls = autoclass('java.lang.String')
        # >>> cls.valueOf.signatures()
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
        result = cls.valueOf.signatures()

        assert isinstance(result, list)
        assert all(isinstance(f, tuple) for f in result)

        assert sorted(result) == sorted([
            (['boolean'], 'java/lang/String'),
            (['char'], 'java/lang/String'),
            (['char[]'], 'java/lang/String'),
            (['char[]', 'int', 'int'], 'java/lang/String'),
            (['double'], 'java/lang/String'),
            (['float'], 'java/lang/String'),
            (['int'], 'java/lang/String'),
            (['java/lang/Object'], 'java/lang/String'),
            (['long'], 'java/lang/String')
        ])
