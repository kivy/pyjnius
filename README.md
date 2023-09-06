PyJNIus
=======

A Python module to access Java classes as Python classes using the Java Native
Interface (JNI).
Warning: the pypi name is now `pyjnius` instead of `jnius`.

[![Tests](https://github.com/kivy/pyjnius/workflows/Continuous%20Integration/badge.svg)](https://github.com/kivy/pyjnius/actions)
[![Tests (x86)](https://github.com/kivy/pyjnius/workflows/Continuous%20Integration%20(x86)/badge.svg)](https://github.com/kivy/pyjnius/actions)
[![Builds](https://github.com/kivy/pyjnius/workflows/Continuous%20Delivery/badge.svg)](https://github.com/kivy/pyjnius/actions)
[![PyPI](https://img.shields.io/pypi/v/pyjnius.svg)]()
[![Backers on Open Collective](https://opencollective.com/kivy/backers/badge.svg)](#backers)
[![Sponsors on Open Collective](https://opencollective.com/kivy/sponsors/badge.svg)](#sponsors)

Installation
------------

```
pip install pyjnius
```

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
>>> print(stack.pop())
world
>>> print(stack.pop())
hello
```

Usage with python-for-android
-----------------------------

* Get [python-for-android](http://github.com/kivy/python-for-android)
* Compile a distribution with kivy (PyJNIus will be automatically added)

Then, you can do this kind of things:

```python
from time import sleep
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable(True)
for x in xrange(20):
    print(Hardware.accelerometerReading())
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

When you use `autoclass`, it will discover all the methods and fields of the
class and resolve them. You may want to declare and use only what you
need. The previous example can be done manually as follows:

```python
from time import sleep
from jnius import MetaJavaClass, JavaClass, JavaMethod, JavaStaticMethod

class Hardware(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'org/renpy/android/Hardware'
    vibrate = JavaStaticMethod('(D)V')
    accelerometerEnable = JavaStaticMethod('(Z)V')
    accelerometerReading = JavaStaticMethod('()[F')
    getDPI = JavaStaticMethod('()I')

# use that new class!
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable()
for x in xrange(20):
    print(Hardware.accelerometerReading())
    sleep(.1)
```

You can use the `signatures` method of `JavaMethod` and `JavaMultipleMethod`, to inspect the discovered signatures of a method of an object

```python
>>> String = autoclass('java.lang.String')
>>> dir(String)
['CASE_INSENSITIVE_ORDER', '__class__', '_JavaClass__cls_storage', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__javaclass__', '__javaconstructor__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__pyx_vtable__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'charAt', 'checkBounds', 'clone', 'codePointAt', 'codePointBefore', 'codePointCount', 'compareTo', 'compareToIgnoreCase', 'concat', 'contains', 'contentEquals', 'copyValueOf', 'empty', 'endsWith', 'equals', 'equalsIgnoreCase', 'finalize', 'format', 'getBytes', 'getChars', 'getClass', 'hashCode', 'indexOf', 'indexOfSupplementary', 'intern', 'isEmpty', 'join', 'lastIndexOf', 'lastIndexOfSupplementary', 'length', 'matches', 'nonSyncContentEquals', 'notify', 'notifyAll', 'offsetByCodePoints', 'regionMatches', 'registerNatives', 'replace', 'replaceAll', 'replaceFirst', 'split', 'startsWith', 'subSequence', 'substring', 'toCharArray', 'toLowerCase', 'toString', 'toUpperCase', 'trim', 'valueOf', 'wait']
>>> String.format.signatures()
[(['java/util/Locale', 'java/lang/String', 'java/lang/Object...'], 'java/lang/String'), (['java/lang/String', 'java/lang/Object...'], 'java/lang/String')]
```
Each pair contains the list of accepted arguments types, and the returned type.

Troubleshooting
---------------

Make sure a Java Development Kit (JDK) is installed on your operating system if
you want to use PyJNIus on desktop. OpenJDK is known to work, and the Oracle
Java JDK should work as well.

On windows, make sure `JAVA_HOME` points to your java installation, so PyJNIus
can locate the `jvm.dll` file allowing it to start java. This shouldn't be
necessary on OSX and Linux, but in case PyJNIus fails to find it, setting
`JAVA_HOME` should help.

Support
-------

If you need assistance, you can ask for help on our mailing list:

* User Group : https://groups.google.com/group/kivy-users
* Email      : kivy-users@googlegroups.com

We also have a Discord server:

[https://chat.kivy.org/](https://chat.kivy.org/)

Contributing
------------

We love pull requests and discussing novel ideas. Check out our
[contribution guide](http://kivy.org/docs/contribute.html) and
feel free to improve PyJNIus.

The following mailing list and IRC channel are used exclusively for
discussions about developing the Kivy framework and its sister projects:

* Dev Group : https://groups.google.com/group/kivy-dev
* Email     : kivy-dev@googlegroups.com

License
-------

PyJNIus is released under the terms of the MIT License. Please refer to the
LICENSE file for more information.


## Backers

Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/kivy#backer)]

<a href="https://opencollective.com/kivy#backers" target="_blank"><img src="https://opencollective.com/kivy/backers.svg?width=890"></a>


## Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/kivy#sponsor)]

<a href="https://opencollective.com/kivy/sponsor/0/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/1/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/2/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/3/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/4/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/5/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/6/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/7/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/8/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/9/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/9/avatar.svg"></a>
