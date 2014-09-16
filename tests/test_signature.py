import unittest

from jnius import autoclass, java_method, PythonJavaClass, cast

from jnius.signatures import *

JObject = autoclass('java/lang/Object')
JString = autoclass('java/lang/String')

class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        super(TestImplemIterator, self).__init__()
        self.collection = collection
        self.index = index

    @java_signature(jboolean, ())
    def hasNext(self):
        return self.index < len(self.collection.data) - 1

    @java_signature(JObject, ())
    def next(self):
        obj = self.collection.data[self.index]
        self.index += 1
        return obj

    @java_signature(jboolean, ())
    def hasPrevious(self):
        return self.index >= 0

    @java_signature(JObject, ())
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        return obj

    @java_signature(jint, ())
    def previousIndex(self):
        return self.index - 1

    @java_signature(JString, ())
    def toString(self):
        return repr(self)

    @java_signature(JObject, (jint, ))
    def get(self, index):
        return self.collection.data[index - 1]

    @java_signature(jvoid, (JObject, ))
    def set(self, obj):
        self.collection.data[self.index - 1] = obj


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__(*args)
        self.data = list(args)

    @java_signature(autoclass("java.util.Iterator"), ())
    def iterator(self):
        it = TestImplemIterator(self)
        return it

    @java_signature(JString, ())
    def toString(self):
        return repr(self)

    @java_signature(jint, ())
    def size(self):
        return len(self.data)

    @java_signature(JObject, (jint,))
    def get(self, index):
        return self.data[index]

    @java_signature(JObject, (jint, JObject))
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @java_signature(JArray(JObject), ())
    def toArray(self):
        return self.data

    @java_signature(autoclass("java.util.ListIterator"), ())
    def listIterator(self):
        it = TestImplemIterator(self)
        return it

    # TODO cover this case of listIterator.
    @java_method('(I)Ljava/util/ListIterator;',
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
        array = pyjlist.toArray



