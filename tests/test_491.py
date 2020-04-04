from unittest import TestCase
from jnius import autoclass


class Test491(TestCase):
    def test_491(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        stack.push('hello')
        stack.push('world')

        self.assertEqual(stack.pop(), 'world')
        self.assertEqual(stack.pop(), 'hello')
