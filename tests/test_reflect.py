from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass
from jnius import cast
from jnius.reflect import identify_hierarchy
from jnius import find_javaclass

def identify_hierarchy_dict(cls, level, concrete=True):
    return({ cls.getName() : level for cls,level in identify_hierarchy(cls, level, concrete) })

class ReflectTest(unittest.TestCase):

    def assertContains(self, d, clsName):
        self.assertTrue(clsName in d, clsName + " was not found in " + str(d))

    def test_hierharchy_queue(self):
        d = identify_hierarchy_dict(find_javaclass("java.util.Queue"), 0, False)
        self.assertContains(d, "java.util.Queue")
        # super interfaces
        self.assertContains(d, "java.util.Collection")
        self.assertContains(d, "java.lang.Iterable")
        # all instantiated interfaces are rooted at Object
        self.assertContains(d, "java.lang.Object")
        maxLevel = max(d.values())
        self.assertEqual(d["java.lang.Object"], maxLevel)
        self.assertEqual(d["java.util.Queue"], 0)
        
    def test_hierharchy_arraylist(self):
        d = identify_hierarchy_dict(find_javaclass("java.util.ArrayList"), 0, True)
        self.assertContains(d, "java.util.ArrayList")# concrete
        self.assertContains(d, "java.util.AbstractCollection")# superclass
        self.assertContains(d, "java.util.Collection")# interface
        self.assertContains(d, "java.lang.Iterable")# interface
        self.assertContains(d, "java.lang.Object")# root
        maxLevel = max(d.values())
        self.assertEqual(d["java.lang.Object"], maxLevel)
        self.assertEqual(d["java.util.ArrayList"], 0)

    def test_class(self):
        lstClz = autoclass("java.util.List")
        self.assertTrue("_class" in dir(lstClz))
        self.assertEqual("java.util.List", lstClz._class.getName())
        alstClz = autoclass("java.util.ArrayList")
        self.assertTrue("_class" in dir(alstClz))
        self.assertEqual("java.util.ArrayList", alstClz._class.getName())
        self.assertEqual("java.util.ArrayList", alstClz().getClass().getName())

    def test_stack(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        self.assertIsInstance(stack, Stack)
        stack.push('hello')
        stack.push('world')
        self.assertEqual(stack.pop(), 'world')
        self.assertEqual(stack.pop(), 'hello')
    
    def test_collection(self):
        HashSet = autoclass('java.util.HashSet')
        aset = HashSet()
        aset.add('hello')
        aset.add('world')
        #check that the __len__ dunder is applied to a Collection not a List
        self.assertEqual(2, len(aset))
        #check that the __len__ dunder is applied to it cast as a Collection
        self.assertEqual(2, len(cast("java.util.Collection", aset)))

    def test_list_interface(self):
        ArrayList = autoclass('java.util.ArrayList')
        words = ArrayList()
        words.add('hello')
        words.add('world')
        self.assertIsNotNone(words.stream())
        self.assertIsNotNone(words.iterator())

    def test_super_interface(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        words.add('hello')
        words.add('world')
        q = cast('java.util.Queue', words)
        self.assertEqual(2, q.size())
        self.assertEqual(2, len(q))
        self.assertIsNotNone(q.iterator())

    def test_super_object(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        words.hashCode()

    def test_super_interface_object(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        q = cast('java.util.Queue', words)
        q.hashCode()

    def test_list_iteration(self):
        ArrayList = autoclass('java.util.ArrayList')
        words = ArrayList()
        words.add('hello')
        words.add('world')
        self.assertEqual(['hello', 'world'], [word for word in words])

