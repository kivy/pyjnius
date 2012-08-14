PyJNIus
=======

description
-----------

Python module to access Java class as Python class, using JNI.

(Work in progress.)

quick overview
--------------

>>> from jnius.reflect import autoclass
>>> autoclass('java.lang.System').out.println('Hello world')
Hello world

>>>Stack = autoclass('java.util.Stack')
>>>stack = Stack()
>>>stack.push('hello')
>>>stack.push('world')
>>>print stack.pop()
world
>>>print stack.pop()
hello