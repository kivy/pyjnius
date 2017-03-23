'''
signatures.py
=============

A handy API for writing JNI signatures easily

Author: chrisjrn

This module aims to provide a more human-friendly API for
wiring up Java proxy methods in PyJnius.

You can use the signature function to produce JNI method
signautures for methods; passing PyJnius JavaClass classes
as return or argument types; provided here are annotations
representing Java's primitive and array times.

Methods can return just a standard primitive type:

>>> signature(jint, ())
'()I'

>>> s.signature(jvoid, [jint])
'(I)V'

Or you can use autoclass proxies to specify Java classes
for return types.

>>> from jnius import autoclass
>>> String = autoclass("java.lang.String")
>>> signature(String, ())
'()Ljava/lang/String;'

'''

__version__ = '0.0.1'

from . import JavaClass
from . import java_method


''' Type specifiers for primitives '''


class _JavaSignaturePrimitive(object):
    _spec = ""


def _MakeSignaturePrimitive(name, spec):
    class __Primitive(_JavaSignaturePrimitive):
        ''' PyJnius signature for Java %s type ''' % name
        _name = name
        _spec = spec
    __Primitive.__name__ = "j" + name

    return __Primitive


jboolean = _MakeSignaturePrimitive("boolean", "Z")
jbyte    = _MakeSignaturePrimitive("byte", "B")
jchar    = _MakeSignaturePrimitive("char", "C")
jdouble  = _MakeSignaturePrimitive("double", "D")
jfloat   = _MakeSignaturePrimitive("float", "F")
jint     = _MakeSignaturePrimitive("int", "I")
jlong    = _MakeSignaturePrimitive("long", "J")
jshort   = _MakeSignaturePrimitive("short", "S")
jvoid    = _MakeSignaturePrimitive("void", "V")


def JArray(of_type):
    ''' Signature helper for identifying arrays of a given object or
    primitive type. '''

    spec = "[" + _jni_type_spec(of_type)
    return _MakeSignaturePrimitive("array", spec)


def with_signature(returns, takes):
    ''' Alternative version of @java_method that takes JavaClass
    objects to produce the method signature. '''

    sig = signature(returns, takes)
    return java_method(sig)


def signature(returns, takes):
    ''' Produces a JNI method signature, taking the provided arguments
    and returning the given return type. '''

    out_takes = []
    for arg in takes:
        out_takes.append(_jni_type_spec(arg))

    return "(" + "".join(out_takes) + ")" + _jni_type_spec(returns)


def _jni_type_spec(jclass):
    ''' Produces a JNI type specification string for the given argument.
    If the argument is a jnius.JavaClass, it produces the JNI type spec
    for the class. Signature primitives return their stored type spec.
    '''

    if issubclass(jclass, JavaClass):
        return "L" + jclass.__javaclass__ + ";"
    elif issubclass(jclass, _JavaSignaturePrimitive):
        return jclass._spec
