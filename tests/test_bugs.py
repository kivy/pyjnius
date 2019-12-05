from jnius import autoclass
from unittest import TestCase

class BugTests(TestCase):

    def test_47(self):
        System = autoclass('java.lang.System')

        # This works:
        System.out.println('Hello World')
        map(System.out.println, ['Hello World'])
        println = System.out.println
        map(println, ['Hello World'])

        class MyClass(object):
            def __init__(self):
                self.println = System.out.println  # Instance variables are fine
        map(MyClass().println, ['Hello World'])

        # This causes an exception:
        class MyClass(object):
            println = System.out.println  # But class variables cause errors
        map(MyClass.println, ['Hello World'])
