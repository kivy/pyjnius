'''
signatures.py
=============

A handy API for writing JNI signatures easily

Author: chrisjrn

'''

__version__ = '0.0.1'

from . import JavaClass
from . import java_method


''' Type specifiers for primitives '''

class _SignaturePrimitive(object):
    _spec = ""

def _MakeSignaturePrimitive(name, spec):
    class __Primitive(_SignaturePrimitive):
        ''' PyJnius signature for Java %s type ''' % name
        _name = name
        _spec = spec
        __name__ = "j" + name
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
    ''' Marks that this is an array of the given Primitive of JavaClass
    type specified. '''
    
    spec = "[" + _jni_type_spec(of_type)
    return _MakeSignaturePrimitive("array", spec)

def java_signature(returns, takes):
    ''' Alternative version of @java_method that takes JavaClass
    objects to produce the method signature. '''

    sig = _produce_sig(returns, takes)
    return java_method(sig)

def _produce_sig(returns, takes):
    ''' Produces a JNI method signature. '''
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
    elif issubclass(jclass, _SignaturePrimitive):
        return jclass._spec
    