from __future__ import absolute_import, unicode_literals
import unittest
from jnius import autoclass, cast, PythonJavaClass, java_method


class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = ['java/util/ListIterator']


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__(*args)
        self.data = list(args)

    @java_method('()I')
    def size(self):
        return len(self.data)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.data[index]

    @java_method('(ILjava/lang/Object;)Ljava/lang/Object;')
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object


class TestIntLongConversion(unittest.TestCase):
    def test_reverse(self):
        '''
        String comparison because values are the same for INT and LONG,
        but only __str__ shows the real difference.
        '''

        Collections = autoclass('java.util.Collections')
        List = autoclass('java.util.List')
        pylist = list(range(10))
        a = TestImplem(*pylist)
        self.assertEqual(a.data, pylist)
        self.assertEqual(str(a.data), '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]')

        # reverse the array, be sure it's converted back to INT!
        Collections.reverse(a)

        # conversion to/from Java objects hides INT/LONG conv on Py2
        # which is wrong to switch between because even Java
        # recognizes INT and LONG types separately (Py3 doesn't)
        self.assertEqual(a.data, list(reversed(pylist)))
        self.assertNotIn('L', str(a.data))
        self.assertEqual(str(a.data), '[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]')


if __name__ == '__main__':
    unittest.main()
