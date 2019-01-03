# pylint: disable=invalid-name
'''
Example of nested ArrayList and passing empty tuple/list to Java functions.
'''

from __future__ import unicode_literals, print_function
from jnius import autoclass, cast  # pylint: disable=import-error

String = autoclass('java.lang.String')
List = autoclass('java.util.List')
Arrays = autoclass('java.util.Arrays')
ArrayList = autoclass('java.util.ArrayList')
JavaArray = autoclass('java.lang.reflect.Array')
Object = autoclass('java.lang.Object')


def sep_print(*args):
    '''
    Separate args because in <80char console (e.g. Windows)
    is the output barely readable with [[, @, ;, ,, ...
    '''
    print(*args)
    print('-' * 10)


# Object based empty ArrayList
jlist = ArrayList()
sep_print(jlist, jlist.toString(), len(jlist))

# String array
str_array = JavaArray.newInstance(String, 3)
for i, item in enumerate(('a', 'b', 'c')):
    str_array[i] = String(item)
sep_print(str_array, len(str_array))

# add the array of strings to the list
jlist.add(str_array)
sep_print(jlist, jlist.toString(), len(jlist))

# create a new ArrayList from String array
str_list = ArrayList(Arrays.asList(str_array))
jlist.add(str_list)
sep_print(jlist, jlist.toString(), len(jlist))

# add an empty Object to ArrayList
jlist.add(Object())
sep_print(jlist, jlist.toString(), len(jlist))

# new ArrayList to wrap everything up
plain_list = ArrayList()
plain_list.add(str_array)
plain_list.add(str_list)
plain_list.add(jlist)
sep_print(plain_list, plain_list.toString(), len(plain_list))
