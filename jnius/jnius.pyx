
'''
Java wrapper
============

With this module, you can create Python class that reflects a Java class, and use
it directly in Python.

Example with static method
--------------------------

Java::

    package org.test;
    public class Hardware {
        static int getDPI() {
            return metrics.densityDpi;
        }
    }

Python::

    class Hardware(JavaClass):
        __metaclass__ = MetaJavaClass
        __javaclass__ = 'org/test/Hardware'
        getDPI = JavaStaticMethod('()I')

    Hardware.getDPI()


Example with instance method
----------------------------

Java::

    package org.test;
    public class Action {
        public String getName() {
            return new String("Hello world")
        }
    }

Python::

    class Action(JavaClass):
        __metaclass__ = MetaJavaClass
        __javaclass__ = 'org/test/Action'
        getName = JavaMethod('()Ljava/lang/String;')

    action = Action()
    print action.getName()
    # will output Hello World


Example with static/instance field
----------------------------------

Java::

    package org.test;
    public class Test {
        public static String field1 = new String("hello");
        public String field2;

        public Test() {
            this.field2 = new String("world");
        }
    }

Python::

    class Test(JavaClass):
        __metaclass__ = MetaJavaClass
        __javaclass__ = 'org/test/Test'

        field1 = JavaStaticField('Ljava/lang/String;')
        field2 = JavaField('Ljava/lang/String;')

    # access directly to the static field
    print Test.field1

    # create the instance, and access to the instance field
    test = Test()
    print test.field2

'''

__all__ = ('JavaObject', 'JavaClass', 'JavaMethod', 'JavaField',
           'JavaStaticMethod', 'JavaStaticField', 'JavaMultipleMethod',
           'MetaJavaBase', 'MetaJavaClass', 'JavaException', 'cast',
           'find_javaclass', 'PythonJavaClass', 'java_method', 'detach')

from libc.stdlib cimport malloc, free
from functools import partial
import sys
import traceback

include "jnius_compat.pxi"
include "jni.pxi"
include "config.pxi"

IF JNIUS_PLATFORM == "android":
    include "jnius_jvm_android.pxi"
ELIF JNIUS_PLATFORM == "win32":
    include "jnius_jvm_desktop.pxi"
ELSE:
    include "jnius_jvm_dlopen.pxi"

# from Cython 3.0, in the MetaJavaClass, this is accessed as _JavaClass__cls_storage
# see https://cython.readthedocs.io/en/latest/src/userguide/migrating_to_cy30.html#class-private-name-mangling
cdef CLS_STORAGE_NAME = '_JavaClass__cls_storage' if JNIUS_CYTHON_3 else '__cls_storage'

include "jnius_env.pxi"
include "jnius_utils.pxi"
include "jnius_conversion.pxi"
include "jnius_localref.pxi"

include "jnius_nativetypes3.pxi"

include "jnius_export_func.pxi"
include "jnius_export_class.pxi"

include "jnius_proxy.pxi"
