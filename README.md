PyJNIus
=======

PyJNIus is a [Python](https://www.python.org/) library for accessing 
[Java](https://www.java.com/) classes using the 
[Java Native Interface](https://docs.oracle.com/javase/8/docs/technotes/guides/jni/)
(JNI). 

PyJNIus is managed by the [Kivy Team](https://kivy.org/about.html) and can be
used with [python-for-android](https://github.com/kivy/python-for-android). 

It can also be used independently of Kivy, on desktop and mobile platforms. 

> [!WARNING]
> The [PyPI](https://pypi.org/) package name is now 
[pyjnius](https://pypi.org/project/pyjnius/) instead of `jnius`.


[![Backers on Open Collective](https://opencollective.com/kivy/backers/badge.svg)](#backers)
[![Sponsors on Open Collective](https://opencollective.com/kivy/sponsors/badge.svg)](#sponsors)
[![GitHub contributors](https://img.shields.io/github/contributors-anon/kivy/pyjnius)](https://github.com/kivy/pyjnius/graphs/contributors)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

![PyPI - Version](https://img.shields.io/pypi/v/pyjnius)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyjnius)

[![Tests](https://github.com/kivy/pyjnius/workflows/Continuous%20Integration/badge.svg)](https://github.com/kivy/pyjnius/actions)
[![Tests (x86)](https://github.com/kivy/pyjnius/workflows/Continuous%20Integration%20(x86)/badge.svg)](https://github.com/kivy/pyjnius/actions)
[![Builds](https://github.com/kivy/pyjnius/workflows/Continuous%20Delivery/badge.svg)](https://github.com/kivy/pyjnius/actions)


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

Then, you can do this kind of thing:

```python
from time import sleep
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable(True)
for x in range(20):
    print(Hardware.accelerometerReading())
    sleep(0.1)
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
for x in range(20):
    print(Hardware.accelerometerReading())
    sleep(0.1)
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

On Windows, make sure `JAVA_HOME` points to your Java installation, so PyJNIus
can locate the `jvm.dll` file allowing it to start Java. This shouldn't be
necessary on macOS and Linux, but in case PyJNIus fails to find it, setting
`JAVA_HOME` should help.

## License

PyJNIus is [MIT licensed](LICENSE), actively developed by a great
community and is supported by many projects managed by the 
[Kivy Organization](https://www.kivy.org/about.html).

## Documentation

[Documentation for this repository](https://pyjnius.readthedocs.io/).

## Support

Are you having trouble using PyJNIus or any of its related projects in the Kivy
ecosystem?
Is there an error you don’t understand? Are you trying to figure out how to use 
it? We have volunteers who can help!

The best channels to contact us for support are listed in the latest 
[Contact Us](https://github.com/kivy/pyjnius/blob/master/CONTACT.md) document.

## Contributing

PyJNIus is part of the [Kivy](https://kivy.org) ecosystem - a large group of
products used by many thousands of developers for free, but it
is built entirely by the contributions of volunteers. We welcome (and rely on) 
users who want to give back to the community by contributing to the project.

Contributions can come in many forms. See the latest 
[Contribution Guidelines](https://github.com/kivy/pyjnius/blob/master/CONTRIBUTING.md)
for how you can help us.

## Code of Conduct

In the interest of fostering an open and welcoming community, we as 
contributors and maintainers need to ensure participation in our project and 
our sister projects is a harassment-free and positive experience for everyone. 
It is vital that all interaction is conducted in a manner conveying respect, 
open-mindedness and gratitude.

Please consult the [latest Code of Conduct](https://github.com/kivy/pyjnius/blob/master/CODE_OF_CONDUCT.md).

## Contributors

This project exists thanks to 
[all the people who contribute](https://github.com/kivy/pyjnius/graphs/contributors).
[[Become a contributor](CONTRIBUTING.md)].

<img src="https://contrib.nn.ci/api?repo=kivy/pyjnius&pages=5&no_bot=true&radius=22&cols=18">

## Backers

Thank you to [all of our backers](https://opencollective.com/kivy)! 
🙏 [[Become a backer](https://opencollective.com/kivy#backer)]

<img src="https://opencollective.com/kivy/backers.svg?width=890&avatarHeight=44&button=false">

## Sponsors

Special thanks to 
[all of our sponsors, past and present](https://opencollective.com/kivy).
Support this project by 
[[becoming a sponsor](https://opencollective.com/kivy#sponsor)].

Here are our top current sponsors. Please click through to see their websites,
and support them as they support us. 

<!--- See https://github.com/orgs/kivy/discussions/15 for explanation of this code. -->
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
<a href="https://opencollective.com/kivy/sponsor/10/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/10/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/11/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/11/avatar.svg"></a>

<a href="https://opencollective.com/kivy/sponsor/12/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/12/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/13/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/13/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/14/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/14/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/15/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/15/avatar.svg"></a>
