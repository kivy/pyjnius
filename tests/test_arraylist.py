from __future__ import absolute_import
import unittest
from jnius import autoclass


class ArrayListTest(unittest.TestCase):

    def test_other_dunders(self):
        alist = autoclass('java.util.ArrayList')()
        args = [1,2]
        for arg in args:
            alist.add(arg)
        self.assertEqual(len(args), len(alist))
        for idx, arg in enumerate(args):
            self.assertTrue(arg in alist)
        del(alist[1])
        del(alist[0])
        self.assertEqual(0, len(alist))

    def test_output(self):
        alist = autoclass('java.util.ArrayList')()
        args = [0, 1, 5, -1, -5, 0.0, 1.0, 5.0, -1.0, -5.0, True, False]

        for arg in args:
            alist.add(arg)
        for idx, arg in enumerate(args):
            if isinstance(arg, bool):
                self.assertEqual(str(alist[idx]), str(int(arg)))
            else:
                self.assertEqual(str(alist[idx]), str(arg))
        self.assertEqual(len(args), len(alist))


if __name__ == '__main__':
    unittest.main()
