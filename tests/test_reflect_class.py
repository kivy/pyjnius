

import unittest
from jnius.reflect import autoclass, reflect_class

class ReflectTest(unittest.TestCase):

    def test_reflect_class(self):
        cls_loader = autoclass("java.lang.ClassLoader").getSystemClassLoader()
        # choose an obscure class that jnius hasnt seen before during unit tests
        cls = cls_loader.loadClass("java.util.zip.CRC32")
        # we get a Class object
        self.assertEqual("java.lang.Class", cls.getClass().getName())
        # which represents CRC32
        self.assertEqual("java.util.zip.CRC32", cls.getName())
        # lets make that into a python obj representing the class
        pyclass = reflect_class(cls)
        # check it refers to the same thing
        self.assertEqual("java/util/zip/CRC32", pyclass.__javaclass__)
        # check we can instantiate it
        instance = pyclass()
        self.assertIsNotNone(instance)