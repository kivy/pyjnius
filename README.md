Phyjnius
========

Phyjnius is a fork of the [kivy/pyjnius](https://github.com/kivy/pyjnius) project. Phyjnius provides a Java-Python bridge to access Java class as Python class, using JNI and Java reflection. Phyjnius aims to provide a "Pythonic" Java-Python bridge that allows Python developers to use Java libraries efficiently and comfortably.

Phyjnius is used by the [ovation](https://github.com/physion/ovation-python) package, a Python API for the [Ovation Scientific Data Management System](ovation.io).


Quick overview
--------------

```python
>>> from jnius import autoclass
>>> autoclass('java.lang.System').out.println('Hello world')
Hello world

>>> Stack = autoclass('java.util.Stack')
>>> stack = Stack()
>>> stack.push('hello')
>>> stack.push('world')
>>> print stack.pop()
world
>>> print stack.pop()
hello
```

Usage
-----

You need a java JDK installed (openjdk will do), cython, and make to build it

    make

That's it! you can run the tests with

    make tests

To make sure everything is running right.


Advanced example
----------------

When you use autoclass, it will discover all the methods and fields within the object, and resolve it.
For now, it can be better to declare and use only what you need.
The previous example can be done manually:

```python
from time import sleep
from java import MetaJavaClass, JavaClass, JavaMethod, JavaStaticMethod

class Hardware(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'org/renpy/android/Hardware'
    vibrate = JavaStaticMethod('(D)V')
    accelerometerEnable = JavaStaticMethod('(Z)V')
    accelerometerReading = JavaStaticMethod('()[F')
    getDPI = JavaStaticMethod('()I')
    
# use that new class!
print 'DPI is', Hardware.getDPI()

Hardware.accelerometerEnable()
for x in xrange(20):
    print Hardware.accelerometerReading()
    sleep(.1)
```

Support/Discussion
------------------

mailto:pyjnius-dev@googlegroups.com

License
--------

Copyright (c) 2013, Physion LLC. Original PyJnius code is copyright its original authors.

Distribution and usage is licensed under the terms of the GNU Lesser General Public License ([LGPL](http://www.gnu.org/licenses/lgpl.html "LGPL")).