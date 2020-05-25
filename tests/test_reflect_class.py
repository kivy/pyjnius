

import unittest
from jnius.reflect import autoclass, reflect_class

class ReflectTest(unittest.TestCase):

    def test_reflect_class(self):
        cls_loader = autoclass("java.lang.ClassLoader").getSystemClassLoader()
        
        # choose an obscure class that jnius hasnt seen before during unit tests
        cls_name = "java.util.zip.CRC32"
        from jnius import MetaJavaClass
        if MetaJavaClass.get_javaclass(cls_name) is not None:
            self.skipTest("%s already loaded - has this test run more than once?" % cls_name)

        cls = cls_loader.loadClass(cls_name)
        # we get a Class object
        self.assertEqual("java.lang.Class", cls.getClass().getName())
        # which represents CRC32
        self.assertEqual(cls_name, cls.getName())
        # lets make that into a python obj representing the class
        pyclass = reflect_class(cls)
        # check it refers to the same thing
        self.assertEqual(cls_name.replace('.', '/'), pyclass.__javaclass__)
        # check we can instantiate it
        instance = pyclass()
        self.assertIsNotNone(instance)