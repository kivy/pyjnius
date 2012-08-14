from jnius import JavaClass, MetaJavaClass, JavaMethod

class HelloWorld(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'org/jnius/HelloWorld'

    hello = JavaMethod('()V')

a = HelloWorld()
a.hello()
