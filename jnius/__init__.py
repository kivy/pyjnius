'''
Pyjnius
=======

Accessing Java classes from Python.

All the documentation is available at: http://pyjnius.readthedocs.org
'''

__version__ = '1.1-dev'

from .jnius import *
from .reflect import *

# XXX monkey patch methods that cannot be in cython.
# Cython doesn't allow to set new attribute on methods it compiled

HASHCODE_MAX = 2 ** 31 - 1

class PythonJavaClass_(PythonJavaClass):

    @java_method('()I', name='hashCode')
    def hashCode(self):
        return id(self) % HASHCODE_MAX

    @java_method('()Ljava/lang/String;', name='hashCode')
    def hashCode_(self):
        return '{}'.format(self.hashCode())

    @java_method('()Ljava/lang/String;', name='toString')
    def toString(self):
        return repr(self)

    @java_method('(Ljava/lang/Object;)Z', name='equals')
    def equals(self, other):
        return self.hashCode() == other.hashCode()

PythonJavaClass = PythonJavaClass_


# from https://gist.github.com/tito/09c42fb4767721dc323d
import threading
orig_thread_run = threading.Thread.run
def thread_check_run(*args, **kwargs):
    try:
       return orig_thread_run(*args, **kwargs)
    finally:
        jnius.detach()
threading.Thread.run = thread_check_run
