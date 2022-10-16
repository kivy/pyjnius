from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius import JavaClass, MetaJavaClass, JavaMethod

class HelloWorldTest(unittest.TestCase):

    def test_helloworld(self):

        class HelloWorld(JavaClass, metaclass=MetaJavaClass):
            __javaclass__ = 'org/jnius/HelloWorld'
            hello = JavaMethod('()Ljava/lang/String;')

        a = HelloWorld()
        self.assertEqual(a.hello(), 'world')
