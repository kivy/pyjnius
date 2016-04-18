PyJNIus
=======

A Python module to access Java classes as Python classes using JNI.

PyJNIus is a "Work In Progress".

[![Build Status](https://travis-ci.org/kivy/pyjnius.svg?branch=master)](https://travis-ci.org/kivy/pyjnius)

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

Usage on desktop
----------------

You need a java JDK installed (OpenJDK will do), Cython and make to build it.
Please ensure that your `JDK_HOME` or `JAVA_HOME` environment variable points
to the installed JDK root directory, and that the JVM library (`jvm.so` or
`jvm.dll`) is available from your `PATH` environment variable. **Failure to do
so may result in a failed install, or a successful install but inability to
use the pyjnius library.**

    make

That's it! You can run the tests using

    make tests

to ensure everything is running correctly.

Usage with python-for-android
-----------------------------

* Get http://github.com/kivy/python-for-android
* Compile a distribution with kivy (pyjnius will be automatically added)
* Then, you can do this kind of thing:

```python
from time import sleep
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')
print 'DPI is', Hardware.getDPI()

Hardware.accelerometerEnable(True)
for x in xrange(20):
    print Hardware.accelerometerReading()
    sleep(.1)
```

It will output something like:

```
I/python  ( 5983): Android kivy bootstrap done. __name__ is __main__
I/python  ( 5983): Run user program, change dir and execute main.py
I/python  ( 5983): DPI is 160
I/python  ( 5983): [0.0, 0.0, 0.0]
I/python  ( 5983): [-0.0095768067985773087, 9.3852710723876953, 2.2218191623687744]
I/python  ( 5983): [-0.0095768067985773087, 9.3948478698730469, 2.2218191623687744]
I/python  ( 5983): [-0.0095768067985773087, 9.3948478698730469, 2.2026655673980713]
I/python  ( 5983): [-0.028730420395731926, 9.4044246673583984, 2.2122423648834229]
I/python  ( 5983): [-0.019153613597154617, 9.3852710723876953, 2.2026655673980713]
I/python  ( 5983): [-0.028730420395731926, 9.3852710723876953, 2.2122423648834229]
I/python  ( 5983): [-0.0095768067985773087, 9.3852710723876953, 2.1835119724273682]
I/python  ( 5983): [-0.0095768067985773087, 9.3756942749023438, 2.1835119724273682]
I/python  ( 5983): [0.019153613597154617, 9.3948478698730469, 2.2122423648834229]
I/python  ( 5983): [0.038307227194309235, 9.3852710723876953, 2.2218191623687744]
I/python  ( 5983): [-0.028730420395731926, 9.3948478698730469, 2.2026655673980713]
I/python  ( 5983): [-0.028730420395731926, 9.3852710723876953, 2.2122423648834229]
I/python  ( 5983): [-0.038307227194309235, 9.3756942749023438, 2.2026655673980713]
I/python  ( 5983): [0.3926490843296051, 9.3086557388305664, 1.3311761617660522]
I/python  ( 5983): [-0.10534487664699554, 9.4331550598144531, 2.1068975925445557]
I/python  ( 5983): [0.26815059781074524, 9.3469638824462891, 2.3463177680969238]
I/python  ( 5983): [-0.1149216815829277, 9.3852710723876953, 2.31758713722229]
I/python  ( 5983): [-0.038307227194309235, 9.41400146484375, 1.8674772977828979]
I/python  ( 5983): [0.13407529890537262, 9.4235782623291016, 2.2026655673980713]
```

Advanced example
----------------

When you use autoclass, it will discover all the methods and fields of the
object and resolve them. For now, it is better to declare and use only what you
need. The previous example can be done manually as follows:

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

Support
-------

If you need assistance, you can ask for help on our mailing list:

* User Group : https://groups.google.com/group/kivy-users
* Email      : kivy-users@googlegroups.com

We also have an IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy

Contributing
------------

We love pull requests and discussing novel ideas. Check out our
[contribution guide](http://kivy.org/docs/contribute.html) and
feel free to improve PyJNIus.

The following mailing list and IRC channel are used exclusively for
discussions about developing the Kivy framework and its sister projects:

* Dev Group : https://groups.google.com/group/kivy-dev
* Email     : kivy-dev@googlegroups.com

IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy-dev

License
-------

PyJNIus is released under the terms of the MIT License. Please refer to the
LICENSE file.
