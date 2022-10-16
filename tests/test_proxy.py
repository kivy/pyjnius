from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from jnius import autoclass, java_method, PythonJavaClass, cast

print('1: declare a TestImplem that implement Collection')


class _TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        #'java/util/Iterator',
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
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

    @java_method('()Z')
    def hasPrevious(self):
        return self.index >= 0

    @java_method('()Ljava/lang/Object;')
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        return obj

    @java_method('()I')
    def previousIndex(self):
        return self.index - 1

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.collection.data[index - 1]

    @java_method('(Ljava/lang/Object;)V')
    def set(self, obj):
        self.collection.data[self.index - 1] = obj


class _TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(_TestImplem, self).__init__(*args)
        self.data = list(args)

    @java_method('()Ljava/util/Iterator;')
    def iterator(self):
        it = _TestImplemIterator(self)
        return it

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('()I')
    def size(self):
        return len(self.data)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.data[index]

    @java_method('(ILjava/lang/Object;)Ljava/lang/Object;')
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @java_method('()[Ljava/lang/Object;')
    def toArray(self):
        return self.data

    @java_method('()Ljava/util/ListIterator;')
    def listIterator(self):
        it = _TestImplemIterator(self)
        return it

    @java_method('(I)Ljava/util/ListIterator;',
                         name='ListIterator')
    def listIteratorI(self, index):
        it = _TestImplemIterator(self, index)
        return it


class _TestBadSignature(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    @java_method('(Landroid/bluetooth/BluetoothDevice;IB[])V')
    def bad_signature(self, *args):
        pass


print('2: instantiate the class, with some data')
a = _TestImplem(*list(range(10)))
print(a)
print(dir(a))

print('tries to get a ListIterator')
iterator = a.listIterator()
print('iterator is', iterator)
while iterator.hasNext():
    print('at index', iterator.index, 'value is', iterator.next())

print('3: Do cast to a collection')
a2 = cast('java/util/Collection', a.j_self)
print(a2)

print('4: Try few method on the collection')
Collections = autoclass('java.util.Collections')
#print Collections.enumeration(a)
#print Collections.enumeration(a)
ret = Collections.max(a)

print("reverse")
print(Collections.reverse(a))
print(a.data)

print("before swap")
print(Collections.swap(a, 2, 3))
print("after swap")
print(a.data)

print("rotate")
print(Collections.rotate(a, 5))
print(a.data)

print('Order of data before shuffle()', a.data)
print(Collections.shuffle(a))
print('Order of data after shuffle()', a.data)


# XXX We have issues for methosd with multiple signature
print('-> Collections.max(a)')
print(Collections.max(a2))
#print '-> Collections.shuffle(a)'
#print Collections.shuffle(a2)

# test bad signature
threw = False
try:
    _TestBadSignature()
except Exception:
    threw = True

if not threw:
    raise Exception("Failed to throw for bad signature")
