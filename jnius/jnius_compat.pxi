'''
Handle Python 2 vs 3 differences here.
'''

from cpython.version cimport PY_MAJOR_VERSION

cdef int PY2 = PY_MAJOR_VERSION < 3

# because Cython's basestring doesn't work with isinstance() properly
# and has differences between Python 2 and Python 3 runtime behavior
# so it's not really usable unless some bug in the upstream is fixed
# (tested with Cython==0.29.2)
cdef tuple base_string
if PY_MAJOR_VERSION < 3:
    base_string = (bytes, unicode)
else:
    base_string = (bytes, str)


cdef unicode to_unicode(object arg):
    '''
    Accept full object as a type to prevent py2/py3 differences
    and throw an exception in case of misusing this function.
    '''

    if not isinstance(arg, base_string):
        raise JavaException(
            'Argument {!r} is not of a text type.'.format(arg)
        )

    cdef unicode result
    if isinstance(arg, bytes):
        result = (<bytes>arg).decode('utf-8')
    else:
        result = arg
    return result
