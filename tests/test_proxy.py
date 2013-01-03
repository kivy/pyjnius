from jnius import autoclass, java_implementation, PythonJavaClass, cast

print '1: declare a TestImplem that implement Collection'


class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        #'java/util/Iterator',
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        super(TestImplemIterator, self).__init__()
        self.collection = collection
        self.index = index

    @java_implementation('()Z')
    def hasNext(self):
        return self.index < len(self.collection.data)

    @java_implementation('()Ljava/lang/Object;')
    def next(self):
        obj = self.collection.data[self.index]
        self.index += 1
        return obj

    @java_implementation('()Z')
    def hasPrevious(self):
        return self.index >= 0

    @java_implementation('()Ljava/lang/Object;')
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        print "previous called", obj
        return obj

    @java_implementation('()I')
    def previousIndex(self):
        return self.index - 1

    @java_implementation('()Ljava/lang/String;')
    def toString(self):
        return repr(self)


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__()
        self.data = list(args)

    @java_implementation('()Ljava/util/Iterator;')
    def iterator(self):
        it = TestImplemIterator(self)
        return it

    @java_implementation('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_implementation('()I')
    def size(self):
        return len(self.data)

    @java_implementation('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.data[index]

    @java_implementation('(ILjava/lang/Object;)Ljava/lang/Object;')
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @java_implementation('()[Ljava/lang/Object;')
    def toArray(self):
        return self.data

    @java_implementation('()Ljava/util/ListIterator;')
    def listIterator(self):
        it = TestImplemIterator(self)
        return it

    @java_implementation('(I)Ljava/util/ListIterator;',
                         name='ListIterator')
    def listIteratorI(self, index):
        it = TestImplemIterator(self, index)
        return it


print '2: instanciate the class, with some data'
a = TestImplem(*range(10))
print a
print dir(a)

print '3: Do cast to a collection'
a2 = cast('java/util/Collection', a.j_self)
print a2

print '4: Try few method on the collection'
Collections = autoclass('java.util.Collections')
#print Collections.enumeration(a)
#print Collections.enumeration(a)
ret = Collections.max(a)
print 'MAX returned', ret

# the first one of the following methods will work, witchever it is
# the next ones will fail
print "reverse"
print Collections.reverse(a)
print a.data

print "reverse"
print Collections.reverse(a)
print a.data

print "before swap"
print Collections.swap(a, 2, 3)
print "after swap"
print a.data

print "rotate"
print Collections.rotate(a, 5)
print a.data

print 'Order of data before shuffle()', a.data
print Collections.shuffle(a)
print 'Order of data after shuffle()', a.data


# XXX We have issues for methosd with multiple signature
#print '-> Collections.max(a)'
#print Collections.max(a2)
#print '-> Collections.max(a)'
#print Collections.max(a2)
#print '-> Collections.shuffle(a)'
#print Collections.shuffle(a2)
