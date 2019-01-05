'''
Check various function arguments to be properly passed to Java function
as an Object that is not `null` except `None` itself.
'''

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from jnius import autoclass, JavaException


ObjectArgument = autoclass('org.jnius.ObjectArgument')


class ArgumentsTest(unittest.TestCase):
    '''
    Tests for function arguments.
    '''

    def test_argument_none(self):
        '''
        Converts Python None to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject(None), -1)

    def test_argument_emptylist(self):
        '''
        Converts Python list to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject([]), 0)

    def test_argument_emptytuple(self):
        '''
        Converts Python tuple to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject(()), 0)

    def test_argument_list_emptylist(self):
        '''
        Converts Python list to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject([[], ]), 0)

    def test_argument_tuple_emptytuple(self):
        '''
        Converts Python tuple to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject(((), )), 0)

    def test_argument_list_none(self):
        '''
        Converts Python list to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject([None, ]), 0)

    def test_argument_tuple_none(self):
        '''
        Converts Python tuple to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject((None, )), 0)

    def test_argument_emptyunicode(self):
        '''
        Converts Python unicode to java.lang.Object.
        '''
        self.assertEqual(ObjectArgument.checkObject(u''), 0)

    def test_argument_emptybytes(self):
        '''
        Converts Python bytes to Java String.
        '''
        self.assertEqual(ObjectArgument.checkObject(b''), 0)


if __name__ == '__main__':
    unittest.main()
