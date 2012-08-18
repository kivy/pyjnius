import unittest
from jnius import JavaClass, MetaJavaClass, JavaMethod

class HelloWorldTest(unittest.TestCase):

    def test_helloworld(self):

        class HelloWorld(JavaClass):
            __metaclass__ = MetaJavaClass
            __javaclass__ = 'org/jnius/HelloWorld'
            hello = JavaMethod('()Ljava/lang/String;')

        a = HelloWorld()
        self.assertEqual(a.hello(), 'world')
