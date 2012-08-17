.. _api:

API
===

.. module:: jnius

This part of the documentation covers all the interfaces of Pyjnius.

Java* Objects
-------------

.. class:: JavaClass

    Base for reflecting a Java class. The idea is to subclass this JavaClass,
    add few :class:`JavaMethod`, :class:`JavaStaticMethod`, :class:`JavaField`,
    :class:`JavaStaticField`, and you're done.

    You need to define at minimun the :data:`__javaclass__` attribute, and set
    the :data:`__metaclass__` to :class:`MetaJavaClass`.

    So the minimun class definition would look like::

        from jnius import JavaClass, MetaJavaClass

        class Stack(JavaClass):
            __javaclass__ = 'java/util/Stack'
            __metaclass__ = MetaJavaClass

    .. attribute:: __metaclass__

        Must be set to :class:`MetaJavaClass`, otherwise, all the
        methods/fields declared will be not linked to the JavaClass.

    .. attribute:: __javaclass__

        Represent the Java class name, in the format org/lang/Class. (eg:
        'java/util/Stack')

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

