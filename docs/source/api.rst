.. _api:

API
===

.. module:: jnius

This part of the documentation covers all the interfaces of Pyjnius.

Reflection classes
------------------

.. class:: JavaClass

    Base for reflecting a Java class. The idea is to subclass this JavaClass,
    add few :class:`JavaMethod`, :class:`JavaStaticMethod`, :class:`JavaField`,
    :class:`JavaStaticField`, and you're done.

    You need to define at minimun the :data:`__javaclass__` attribute, and set
    the :data:`__metaclass__` to :class:`MetaJavaClass`.

    So the minimum class definition would look like::

        from jnius import JavaClass, MetaJavaClass

        class Stack(JavaClass):
            __javaclass__ = 'java/util/Stack'
            __metaclass__ = MetaJavaClass

    .. attribute:: __metaclass__

        Must be set to :class:`MetaJavaClass`, otherwise, all the
        methods/fields declared will be not linked to the JavaClass.

    .. attribute:: __javaclass__

        Represent the Java class name, in the format 'org/lang/Class'. (eg:
        'java/util/Stack'), not 'org.lang.Class'.

    .. attribute:: __javaconstructor__

        If not set, we assume the default constructor to take no parameters.
        Otherwise, it can be a list of all possible signatures of the
        constructor. For example, a reflection of the String java class would
        look like::

            class String(JavaClass):
                __javaclass__ == 'java/lang/String'
                __metaclass__ = MetaJavaClass
                __javaconstructor__ == (
                    '()V',
                    '(Ljava/lang/String;)V',
                    '([C)V',
                    '([CII)V',
                    # ...
                )

.. class:: JavaMethod

    Reflection of a Java method.

    .. method:: __init__(signature, static=False)

        Create a reflection of a Java method. The signature is in the JNI
        format. For example::

            class Stack(JavaClass):
                __javaclass__ = 'java/util/Stack'
                __metaclass__ = MetaJavaClass

                peek = JavaMethod('()Ljava/lang/Object;')
                empty = JavaMethod('()Z')

        The name associated to the method is automatically set from the
        declaration within the JavaClass itself.

        The signature can be found with the `javap -s`. For example, if you
        want to fetch the signatures available for `java.util.Stack`::

            $ javap -s java.util.Stack
            Compiled from "Stack.java"
            public class java.util.Stack extends java.util.Vector{
            public java.util.Stack();
              Signature: ()V
            public java.lang.Object push(java.lang.Object);
              Signature: (Ljava/lang/Object;)Ljava/lang/Object;
            public synchronized java.lang.Object pop();
              Signature: ()Ljava/lang/Object;
            public synchronized java.lang.Object peek();
              Signature: ()Ljava/lang/Object;
            public boolean empty();
              Signature: ()Z
            public synchronized int search(java.lang.Object);
              Signature: (Ljava/lang/Object;)I
            }


.. class:: JavaStaticMethod

    Reflection of a static Java method.


.. class:: JavaField

    Reflection of a Java field.

    .. method:: __init__(signature, static=False)

        Create a reflection of a Java field. The signature is in the JNI
        format. For example::

            class System(JavaClass):
                __javaclass__ = 'java/lang/System'
                __metaclass__ = MetaJavaClass

                out = JavaField('()Ljava/io/InputStream;', static=True)

        The name associated to the method is automatically set from the
        declaration within the JavaClass itself.


.. class:: JavaStaticField

    Reflection of a static Java field


.. class:: JavaMultipleMethod

    Reflection of a Java method that can be called from multiple signatures.
    For example, the method `getBytes` in the `String` class can be called
    from::

        public byte[] getBytes(java.lang.String)
        public byte[] getBytes(java.nio.charset.Charset)
        public byte[] getBytes()

    Let's see how you could declare that method::

        class String(JavaClass):
            __javaclass__ = 'java/lang/String'
            __metaclass__ = MetaJavaClass

            getBytes = JavaMultipleMethod([
                '(Ljava/lang/String;)[B',
                '(Ljava/nio/charset/Charset;)[B',
                '()[B'])

    Then, when you will try to access to this method, we'll take the best
    method available according to the type of the arguments you're using.
    Internally, we are calculating a "match" score for each available
    signature, and take the best one. Without going into the details, the score
    calculation look like:

    * a direct type match is +10
    * a indirect type match (like using a `float` for an `int` argument) is +5
    * object with unknown type (:class:`JavaObject`) is +1
    * otherwise, it's considered as an error case, and return -1


Reflection functions
--------------------

.. function:: autoclass(name)

    Return a :class:`JavaClass` that represent the class passed from `name`.
    The name must be written in the format: `a.b.c`, not `a/b/c`.

    >>> from jnius import autoclass
    >>> autoclass('java.lang.System')
    <class 'jnius.reflect.java.lang.System'>

