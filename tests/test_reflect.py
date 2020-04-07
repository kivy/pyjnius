from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass
from jnius import cast

class ReflectTest(unittest.TestCase):

    def test_stack(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        self.assertIsInstance(stack, Stack)
        stack.push('hello')
        stack.push('world')
        self.assertEqual(stack.pop(), 'world')
        self.assertEqual(stack.pop(), 'hello')
    
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

