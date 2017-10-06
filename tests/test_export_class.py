from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius import autoclass, java_method, PythonJavaClass

Iterable = autoclass('java.lang.Iterable')
ArrayList = autoclass('java.util.ArrayList')
Runnable = autoclass('java.lang.Runnable')
Thread = autoclass('java.lang.Thread')
Object = autoclass('java.lang.Object')

class SampleIterable(PythonJavaClass):
    __javainterfaces__ = ['java/lang/Iterable']

    @java_method('()Ljava/lang/Iterator;')
    def iterator(self):
        sample = ArrayList()
        sample.add(1)
        sample.add(2)
        return sample.iterator()

class ExportClassTest(unittest.TestCase):
    def test_is_instance(self):
        array_list = ArrayList()
        thread = Thread()
        sample_iterable = SampleIterable()

        self.assertIsInstance(sample_iterable, Iterable)
        self.assertIsInstance(sample_iterable, Object)
        self.assertIsInstance(sample_iterable, SampleIterable)
        self.assertNotIsInstance(sample_iterable, Runnable)
        self.assertNotIsInstance(sample_iterable, Thread)

        self.assertIsInstance(array_list, Iterable)
        self.assertIsInstance(array_list, ArrayList)
        self.assertIsInstance(array_list, Object)

        self.assertNotIsInstance(thread, Iterable)
        self.assertIsInstance(thread, Thread)
        self.assertIsInstance(thread, Runnable)

    def test_subclasses_work_for_arg_matching(self):
        array_list = ArrayList()
        array_list.add(SampleIterable())
        self.assertIsInstance(array_list.get(0), Iterable)
        self.assertIsInstance(array_list.get(0), SampleIterable)


    def assertIsSubclass(self, cls, parent):
        if not issubclass(cls, parent):
            self.fail("%s is not a subclass of %s" %
                      (cls.__name__, parent.__name__))

    def assertNotIsSubclass(self, cls, parent):
        if issubclass(cls, parent):
            self.fail("%s is a subclass of %s" %
                      (cls.__name__, parent.__name__))

    def test_is_subclass(self):
        self.assertIsSubclass(Thread, Runnable)
        self.assertIsSubclass(ArrayList, Iterable)
        self.assertIsSubclass(ArrayList, Object)
        self.assertIsSubclass(SampleIterable, Iterable)
        self.assertNotIsSubclass(Thread, Iterable)
        self.assertNotIsSubclass(ArrayList, Runnable)
        self.assertNotIsSubclass(Runnable, Thread)
        self.assertNotIsSubclass(Iterable, SampleIterable)
