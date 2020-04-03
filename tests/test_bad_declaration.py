from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
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

    def test_java_exception_handling(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        try:
            stack.pop()
            self.fail("Expected exception to be thrown")
        except JavaException as je:
            # print "Got JavaException: " + str(je)
            # print "Got Exception Class: " + je.classname
            # print "Got stacktrace: \n" + '\n'.join(je.stacktrace)
            self.assertEqual("java.util.EmptyStackException", je.classname)

    def test_java_exception_chaining(self):
        BasicsTest = autoclass('org.jnius.BasicsTest')
        basics = BasicsTest()
        try:
            basics.methodExceptionChained()
            self.fail("Expected exception to be thrown")
        except JavaException as je:
            # print "Got JavaException: " + str(je)
            # print "Got Exception Class: " + je.classname
            # print "Got Exception Message: " + je.innermessage
            # print "Got stacktrace: \n" + '\n'.join(je.stacktrace)
            self.assertEqual("java.lang.IllegalArgumentException", je.classname)
            self.assertEqual("helloworld2", je.innermessage)
            self.assertIn("Caused by:", je.stacktrace)
            self.assertEqual(11, len(je.stacktrace))
