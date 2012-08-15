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
