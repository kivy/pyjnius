import unittest

from jnius import autoclass, java_method, PythonJavaClass, cast

from jnius.signatures import *

JObject = autoclass('java/lang/Object')
JString = autoclass('java/lang/String')
JListIterator = autoclass("java.util.ListIterator")

class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        super(TestImplemIterator, self).__init__()
        self.collection = collection
        self.index = index

    @with_signature(jboolean, [])
    def hasNext(self):
        return self.index < len(self.collection.data) - 1

    @with_signature(JObject, [])
    def next(self):
        obj = self.collection.data[self.index]
        self.index += 1
        return obj

    @with_signature(jboolean, [])
    def hasPrevious(self):
        return self.index >= 0

    @with_signature(JObject, [])
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        return obj

    @with_signature(jint, [])
    def previousIndex(self):
        return self.index - 1

    @with_signature(JString, [])
    def toString(self):
        return repr(self)

    @with_signature(JObject, [jint])
    def get(self, index):
        return self.collection.data[index - 1]

    @with_signature(jvoid, [JObject])
    def set(self, obj):
        self.collection.data[self.index - 1] = obj


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__(*args)
        self.data = list(args)

    @with_signature(autoclass("java.util.Iterator"), [])
    def iterator(self):
        it = TestImplemIterator(self)
        return it

    @with_signature(JString, [])
    def toString(self):
        return repr(self)

    @with_signature(jint, [])
    def size(self):
        return len(self.data)

    @with_signature(JObject, [jint])
    def get(self, index):
        return self.data[index]

    @with_signature(JObject, [jint, JObject])
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @with_signature(JArray(JObject), [])
    def toArray(self):
        return self.data

    @with_signature(JListIterator, [])
    def listIterator(self):
        it = TestImplemIterator(self)
        return it

    # TODO cover this case of listIterator.
    @java_method(signature(JListIterator, [jint]),
                         name='ListIterator')
    def listIteratorI(self, index):
        it = TestImplemIterator(self, index)
        return it


from jnius.reflect import autoclass

class SignaturesTest(unittest.TestCase):

    def test_construct_stack_from_testimplem(self):
        Stack = autoclass("java.util.Stack")
        pyjlist = TestImplem(1, 2, 3, 4, 5, 6, 7)
        stack = Stack()
        stack.addAll(pyjlist)
        self.assertEquals(7, pyjlist.size())
        self.assertEquals(stack.size(), pyjlist.size())
        array = pyjlist.toArray()

    def test_return_types(self):

        # Void
        sig = signature(jvoid, [])
        self.assertEquals(sig, "()V")

        # Boolean
        sig = signature(jboolean, [])
        self.assertEquals(sig, "()Z")

        # Byte
        sig = signature(jbyte, [])
        self.assertEquals(sig, "()B")

        # Char
        sig = signature(jchar, [])
        self.assertEquals(sig, "()C")

        # Double
        sig = signature(jdouble, [])
        self.assertEquals(sig, "()D")

        # Float
        sig = signature(jfloat, [])
        self.assertEquals(sig, "()F")

        # Int 
        sig = signature(jint, [])
        self.assertEquals(sig, "()I")

        # Long 
        sig = signature(jlong, [])
        self.assertEquals(sig, "()J")

        # Short 
        sig = signature(jshort, [])
        self.assertEquals(sig, "()S")

        # Object return method
        String = autoclass("java.lang.String")
        sig = signature(String, [])
        self.assertEquals(sig, "()Ljava/lang/String;")

        # Array return
        sig = signature(JArray(jint), [])
        self.assertEquals(sig, "()[I")

    def test_params(self):
        String = autoclass("java.lang.String")

        # Return void, takes objects as parameters
        sig = signature(jvoid, [String, String])
        self.assertEquals(sig, "(Ljava/lang/String;Ljava/lang/String;)V")

        # Multiple array parameter types
        sig = signature(jvoid, [JArray(jint), JArray(jboolean)])
        self.assertEquals(sig, "([I[Z)V")

