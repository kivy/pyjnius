
.. _api:

API
===

.. module:: jnius

This part of the documentation covers all the interfaces of Pyjnius.

Reflection classes
------------------

.. class:: JavaClass

    Base for reflecting a Java class, allowing access to that Java class from Python. 
    The idea is to subclass this JavaClass, add few :class:`JavaMethod`, 
    :class:`JavaStaticMethod`, :class:`JavaField`, :class:`JavaStaticField`, and 
    you're done.

    You need to define at minimum the :data:`__javaclass__` attribute, and set
    the :data:`__metaclass__` to :class:`MetaJavaClass`.

    So the minimum class definition would look like::

        from jnius import JavaClass, MetaJavaClass

        class Stack(JavaClass):
            __javaclass__ = 'java/util/Stack'
            __metaclass__ = MetaJavaClass

    .. attribute:: __metaclass__

        Must be set to :class:`MetaJavaClass`, otherwise, all the
        methods/fields declared will be not linked to the JavaClass.

        .. note::

            Make sure to choose the right metaclass specifier. In Python 2
            there is ``__metaclass__`` class attribute, in Python 3 there is
            a new syntax ``class Stack(JavaClass, metaclass=MetaJavaClass)``.

            For more info see `PEP 3115
            <https://www.python.org/dev/peps/pep-3115/>`_.

    .. attribute:: __javaclass__

        Represents the Java class name, in the format 'org/lang/Class' (e.g.
        'java/util/Stack'), not 'org.lang.Class'.

    .. attribute:: __javaconstructor__

        If not set, we assume the default constructor takes no parameters.
        Otherwise, it can be a list of all possible signatures of the
        constructor. For example, a reflection of the String java class would
        look like::

            class String(JavaClass):
                __javaclass__ = 'java/lang/String'
                __metaclass__ = MetaJavaClass
                __javaconstructor__ = (
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

        The name associated with the method is automatically set from the
        declaration within the JavaClass itself.

        The signature can be found with `javap -s`. For example, if you
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

    Reflection of a static Java field.


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

    Then, when you try to access this method, it will choose the best
    method available according to the type of the arguments you're using.
    Internally, we calculate a "match" score for each available
    signature, and take the best one. Without going into the details, the score
    calculation looks something like:

    * a direct type match is +10
    * a indirect type match (like using a `float` for an `int` argument) is +5
    * object with unknown type (:class:`JavaObject`) is +1
    * otherwise, it's considered as an error case, and returns -1


Reflection functions
--------------------

.. function:: autoclass(name, include_protected=True, include_private=True)

    Return a :class:`JavaClass` that represents the class passed from `name`.
    The name must be written in the format `a.b.c`, not `a/b/c`.

    By default, autoclass will include all fields and methods at all levels of
    the inheritance hierarchy. Use the `include_protected` and `include_private`
    parameters to limit visibility.

    >>> from jnius import autoclass
    >>> autoclass('java.lang.System')
    <class 'jnius.reflect.java.lang.System'>

    autoclass can also represent a nested Java class:

    >>> autoclass('android.provider.Settings$Secure')
    <class 'jnius.reflect.android.provider.Settings$Secure'>

    .. note::
        If a field and a method have the same name, the field will take
        precedence.

    .. note::
        There are sometimes cases when a Java class contains a member that is
        a Python keyword (such as `from`, `class`, etc). You will need to use
        `getattr()` to access the member and then you will be able to call it::

            from jnius import autoclass
            func_from = getattr(autoclass('some.java.Class'), 'from')
            func_from()

        There is also a special case for a `SomeClass.class` class literal
        which you will find either as a result of `SomeClass.getClass()`
        or in the `__javaclass__` python attribute.

    .. warning::
        Currently `SomeClass.getClass()` returns a different Python object,
        therefore to safely compare whether something is the same class in
        Java use `A.hashCode() == B.hashCode()`.

Java class implementation in Python
-----------------------------------

.. class:: PythonJavaClass

    Base for creating a Java class from a Python class. This allows us to
    implement java interfaces completely in Python, and pass such a Python 
    object back to Java.
    
    In reality, you'll create a Python class that mimics the list of declared
    :data:`__javainterfaces__`. When you give an instance of this class to
    Java, Java will just accept it and call the interface methods as declared.
    Under the hood, we are catching the call, and redirecting it to use your
    declared Python method.

    Your class will act as a Proxy to the Java interfaces.

    You need to define at minimum the :data:`__javainterfaces__` attribute, and
    declare java methods with the :func:`java_method` decorator.

    .. note::

        Static methods and static fields are not supported.
        
        You can only implement Java interfaces. You cannot sub-class a java 
        object.
        
        You must retain a reference to the Python object for the entire liftime
        that your object is in-use within java.

    For example, you could implement the `java/util/ListIterator` interface in
    Python like this::

        from jnius import PythonJavaClass, java_method

        class PythonListIterator(PythonJavaClass):
            __javainterfaces__ = ['java/util/ListIterator']

            def __init__(self, collection, index=0):
                super(PythonListIterator, self).__init__()
                self.collection = collection
                self.index = index

            @java_method('()Z')
            def hasNext(self):
                return self.index < len(self.collection.data) - 1

            @java_method('()Ljava/lang/Object;')
            def next(self):
                obj = self.collection.data[self.index]
                self.index += 1
                return obj

            # etc...

    .. attribute:: __javainterfaces__

        List of the Java interfaces you want to proxify, in the format
        'org/lang/Class' (e.g. 'java/util/Iterator'), not 'org.lang.Class'.

    .. attribute:: __javacontext__

        Indicate which class loader to use, 'system' or 'app'. The default is
        'system'.

        - By default, we assume that you are going to implement a Java
          interface declared in the Java API. It will use the 'system' class
          loader.
        - On android, all the java interfaces that you ship within the APK are
          not accessible with the system class loader, but with the application
          thread class loader. So if you wish to implement a class from an
          interface you've done in your app, use 'app'.

.. function:: java_method(java_signature, name=None)

    Decoration function to use with :class:`PythonJavaClass`. The
    `java_signature` must match the wanted signature of the interface. The
    `name` of the method will be the name of the Python method by default. You
    can still force it, in case of multiple signature with the same Java method
    name.
    
    For example::

        class PythonListIterator(PythonJavaClass):
            __javainterfaces__ = ['java/util/ListIterator']
            
            @java_method('()Ljava/lang/Object;')
            def next(self):
                obj = self.collection.data[self.index]
                self.index += 1
                return obj

    Another example with the same Java method name, but 2 differents signatures::
    
        class TestImplem(PythonJavaClass):
            __javainterfaces__ = ['java/util/List']

            @java_method('()Ljava/util/ListIterator;')
            def listIterator(self):
                return PythonListIterator(self)

            @java_method('(I)Ljava/util/ListIterator;',
                                 name='ListIterator')
            def listIteratorWithIndex(self, index):
                return PythonListIterator(self, index)

Java signature format
---------------------

Java signatures have a special format that could be difficult to understand at
first. Let's look at the details. A signature is in the format::

    (<argument1><argument2><...>)<return type>

All the types for any part of the signature can be one of:

* L<java class>; = represent a Java object of the type <java class>
* Z = represent a java/lang/Boolean;
* B = represent a java/lang/Byte;
* C = represent a java/lang/Character;
* S = represent a java/lang/Short;
* I = represent a java/lang/Integer;
* J = represent a java/lang/Long;
* F = represent a java/lang/Float;
* D = represent a java/lang/Double;
* V = represent void, available only for the return type

All the types can have the `[` prefix to indicate an array. The return type can be `V` or empty.

A signature like::

    (ILjava/util/List;)V
    -> argument 1 is an integer
    -> argument 2 is a java.util.List object
    -> the method doesn't return anything.

    (java.util.Collection;[java.lang.Object;)V
    -> argument 1 is a Collection
    -> argument 2 is an array of Object
    -> nothing is returned

    ([B)Z
    -> argument 1 is a Byte []
    -> a boolean is returned
    

When you implement Java in Python, the signature of the Java method must match.
Java provides a tool named `javap` to get the signature of any java class. For
example::

    $ javap -s java.util.Iterator
    Compiled from "Iterator.java"
    public interface java.util.Iterator{
    public abstract boolean hasNext();
      Signature: ()Z
    public abstract java.lang.Object next();
      Signature: ()Ljava/lang/Object;
    public abstract void remove();
      Signature: ()V
    }

The signature for methods of any android class can be easily seen by following these
steps::

    1. $ cd path/to/android/sdk/
    2. $ cd platforms/android-xx/  # Replace xx with your android version
    3. $ javap -s -classpath android.jar android.app.Activity  # Replace android.app.Activity with any android class whose methods' signature you want to see


Java Lambda implementation in Python using Lambdas and Function References
--------------------------------------------------------------------------

It is possible to use Python lambdas or function references to implement Java `functional interfaces <https://docs.oracle.com/javase/8/docs/api/java/util/function/package-summary.html#package.description>`. A functional interface has one (non-default) method. When implementing a functional interface in Python, your lambda must have the correct number of parameters and return the correct data type. You must hold a reference to the Python lambda for as long as it will be used by Java.

For example, here we use a Python lambda to implement the `Comparator <https://docs.oracle.com/javase/8/docs/api/java/util/Comparator.html>` functional interface::

    numbers = autoclass('java.util.ArrayList')()
    Collections = autoclass('java.util.Collections')
    numbers.add(1)
    numbers.add(3)
    revSort = lambda i, j: j - i
    Collections.sort(numbers, revSort)

The lambda is wrapped in a PythonJavaClass, which implements the Java interface of the parameter in the called Java method.

Passing Variables: By Reference or By Value

When Python objects such as `lists` or `bytearrays` are passed to Java Functions, they are converted
to Java arrays. Since Python does not share the same memory space as the JVM, a copy of the data
needs to be made to pass the data.

Consider that the Java method might change values in the Java array. If the Java method had been
called from another Java method, the other Java method would see the value changes because the
parameters are passed by reference. The two methods share the same memory space. Only one copy of
the array data exists.

In Pyjnius, Python calls to Java methods simulate pass by reference by copying the variable values
from the JVM back to Python. This extra copying will have a performance impact for large data
structures. To skip the extra copy and pass by value, use the named parameter `pass_by_reference`.

    obj.method(param1, param2, param3, pass_by_reference=False)

Since Java does not have function named parameters like Python does, they are interpreted by Pyjnius
and are not passed to the Java method.

In the above example, the `pass_by_reference` parameter will apply to all the parameters. For more
control you can pass a `list` or `tuple` instead.

    obj.method(param1, param2, param3, pass_by_reference=(False, True, False))

If the passed `list` or `tuple` is too short, the final value in the series is used for the
remaining parameters.


JVM options and the class path
------------------------------

JVM options need to be set before `import jnius` is called, as they cannot be changed after the VM starts up.
To this end, you can::

    import jnius_config
    jnius_config.add_options('-Xrs', '-Xmx4096')
    jnius_config.set_classpath('.', '/usr/local/fem/plugins/*')
    import jnius

If a classpath is set with these functions, it overrides any CLASSPATH environment variable.
Multiple options or path entries should be supplied as multiple arguments to the `add_` and `set_` functions.
If no classpath is provided and CLASSPATH is not set, the path defaults to `'.'`.
This functionality is not available on Android.


Pyjnius and threads
-------------------

.. function:: detach()

    Each time you create a native thread in Python and use Pyjnius, any call to
    Pyjnius methods will force attachment of the native thread to the current JVM.
    But you must detach it before leaving the thread, and Pyjnius cannot do it for
    you.

Pyjnius automatically calls this `detach()` function for you when a python thread exits. This is done by
monkey-patching the default `run()` method of `threading.Thread` class.

So if you entirely override `run()` from your own subclass of Thread, you must call `detach()` yourself
on any kind of termination.

Example::

    import threading
    import jnius

    class MyThread(threading.Thread):

        def run(...):
            try:
                # use pyjnius here
            finally:
                jnius.detach()


If you don't, it will crash on dalvik and ART / Android::

    D/dalvikvm(16696): threadid=12: thread exiting, not yet detached (count=0)
    D/dalvikvm(16696): threadid=12: thread exiting, not yet detached (count=1)
    E/dalvikvm(16696): threadid=12: native thread exited without detaching
    E/dalvikvm(16696): VM aborting

Or::

    W/art     (21168): Native thread exiting without having called DetachCurrentThread (maybe it's going to use a pthread_key_create destructor?): Thread[16,tid=21293,Native,Thread*=0x4c25c040,peer=0x677eaa70,"Thread-16219"]
    F/art     (21168): art/runtime/thread.cc:903] Native thread exited without calling DetachCurrentThread: Thread[16,tid=21293,Native,Thread*=0x4c25c040,peer=0x677eaa70,"Thread-16219"]
    F/art     (21168): art/runtime/runtime.cc:203] Runtime aborting...
    F/art     (21168): art/runtime/runtime.cc:203] (Aborting thread was not attached to runtime!)
    F/art     (21168): art/runtime/runtime.cc:203] Dumping all threads without appropriate locks held: thread list lock mutator lock
    F/art     (21168): art/runtime/runtime.cc:203] All threads:
    F/art     (21168): art/runtime/runtime.cc:203] DALVIK THREADS (16):
    ...
