import unittest
from jnius import JavaException, JavaClass
from jnius.reflect import autoclass

class BadDeclarationTest(unittest.TestCase):

    def test_class_not_found(self):
        #self.assertRaises(JavaException, autoclass, 'org.unknow.class')
        #self.assertRaises(JavaException, autoclass, 'java/lang/String')
        pass

    def test_invalid_attribute(self):
        Stack = autoclass('java.util.Stack')
        self.assertRaises(AttributeError, getattr, Stack, 'helloworld')

    def test_invalid_static_call(self):
        Stack = autoclass('java.util.Stack')
        self.assertRaises(JavaException, Stack.push, 'hello')

    def test_with_too_much_arguments(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        self.assertRaises(JavaException, stack.push, 'hello', 'world', 123)
