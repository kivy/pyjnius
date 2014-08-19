import unittest
import sys
from jnius import JavaClass, MetaJavaClass, JavaMethod


if sys.version_info < (3, 0):
    code = """class HelloWorld(JavaClass):
        __metaclass__ = MetaJavaClass
        __javaclass__ = 'org/jnius/HelloWorld'
        hello = JavaMethod('()Ljava/lang/String;')"""
else:
    code = """class HelloWorld(JavaClass, metaclass=MetaJavaClass):
        __javaclass__ = 'org/jnius/HelloWorld'
        hello = JavaMethod('()Ljava/lang/String;')"""

exec(code)

class HelloWorldTest(unittest.TestCase):

    def test_helloworld(self):
        a = HelloWorld()
        self.assertEqual(a.hello(), 'world')
