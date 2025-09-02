import unittest

from jnius import autoclass, java_method, PythonJavaClass, cast

from jnius.signatures import *

JObject = autoclass('java/lang/Object')
JString = autoclass('java/lang/String')
JListIterator = autoclass("java.util.ListIterator")

class _TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        super(_TestImplemIterator, self).__init__()
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


class _TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(_TestImplem, self).__init__(*args)
        self.data = list(args)

    @with_signature(autoclass("java.util.Iterator"), [])
    def iterator(self):
        it = _TestImplemIterator(self)
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
        it = _TestImplemIterator(self)
        return it

    # TODO cover this case of listIterator.
    @java_method(signature(JListIterator, [jint]),
                         name='ListIterator')
    def listIteratorI(self, index):
        it = _TestImplemIterator(self, index)
        return it


from jnius.reflect import autoclass

class SignaturesTest(unittest.TestCase):

    def test_construct_stack_from_testimplem(self):
        Stack = autoclass("java.util.Stack")
        pyjlist = _TestImplem(1, 2, 3, 4, 5, 6, 7)
        stack = Stack()
        stack.addAll(pyjlist)
        self.assertEqual(7, pyjlist.size())
        self.assertEqual(stack.size(), pyjlist.size())
        array = pyjlist.toArray()

    def test_return_types(self):

        # Void
        sig = signature(jvoid, [])
        self.assertEqual(sig, "()V")

        # Boolean
        sig = signature(jboolean, [])
        self.assertEqual(sig, "()Z")

        # Byte
        sig = signature(jbyte, [])
        self.assertEqual(sig, "()B")

        # Char
        sig = signature(jchar, [])
        self.assertEqual(sig, "()C")

        # Double
        sig = signature(jdouble, [])
        self.assertEqual(sig, "()D")

        # Float
        sig = signature(jfloat, [])
        self.assertEqual(sig, "()F")

        # Int
        sig = signature(jint, [])
        self.assertEqual(sig, "()I")

        # Long
        sig = signature(jlong, [])
        self.assertEqual(sig, "()J")

        # Short
        sig = signature(jshort, [])
        self.assertEqual(sig, "()S")

        # Object return method
        String = autoclass("java.lang.String")
        sig = signature(String, [])
        self.assertEqual(sig, "()Ljava/lang/String;")

        # Array return
        sig = signature(JArray(jint), [])
        self.assertEqual(sig, "()[I")

    def test_params(self):
        String = autoclass("java.lang.String")

        # Return void, takes objects as parameters
        sig = signature(jvoid, [String, String])
        self.assertEqual(sig, "(Ljava/lang/String;Ljava/lang/String;)V")

        # Multiple array parameter types
        sig = signature(jvoid, [JArray(jint), JArray(jboolean)])
        self.assertEqual(sig, "([I[Z)V")

    def test_calc_signature(self):
        import sys
        clz = autoclass("org.jnius.SignatureTest$IntOrLong")
        obj = clz(0, debug=True) # could be int or long
        # this isnt truly deterministic, the two possible methods are tied for score
        self.assertTrue(obj.was_long)
        
        obj = clz(sys.maxsize)
        self.assertTrue(obj.was_long)

        obj = clz(-1 * sys.maxsize)
        self.assertTrue(obj.was_long)
    
        clz = autoclass("org.jnius.SignatureTest$ShortOrLong")
        # short and long would be tied, 0 could be short or long
        obj = clz(0, signature="(S)V") # so lets tell it is a short
        self.assertTrue(obj.was_short)

        obj = clz(0, signature="(J)V") # lets tell it is a long
        self.assertFalse(obj.was_short)

        obj = clz(sys.maxsize) # this should be a long
        self.assertFalse(obj.was_short)

        autoclass("org.jnius.SignatureTest$ShortOnly")(0) # this should work as short
        autoclass("org.jnius.SignatureTest$ShortOnly")(0.) # this float should be cast to short