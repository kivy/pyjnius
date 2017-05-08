from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass

class ReflectTest(unittest.TestCase):

    def test_stack(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        self.assertIsInstance(stack, Stack)
        stack.push('hello')
        stack.push('world')
        self.assertEqual(stack.pop(), 'world')
        self.assertEqual(stack.pop(), 'hello')

    def test_list_iteration(self):
        ArrayList = autoclass('java.util.ArrayList')
        words = ArrayList()
        words.add('hello')
        words.add('world')
        self.assertEqual(['hello', 'world'], [word for word in words])
