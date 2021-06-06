

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


    def test_dynamic_jar(self):
        # the idea behind this test is to:
        # 1. load an external jar file using an additional ClassLoader
        # 2. check we can instantate the Class instance
        # 3. check we can reflect the Class instance
        # 4. check we can call a method that returns an object that can only be accessed using the additional ClassLoader
        jar_url = "https://repo1.maven.org/maven2/commons-io/commons-io/2.6/commons-io-2.6.jar"
        url = autoclass("java.net.URL")(jar_url)
        sys_cls_loader = autoclass("java.lang.ClassLoader").getSystemClassLoader()
        new_cls_loader = autoclass("java.net.URLClassLoader").newInstance([url], sys_cls_loader)
        cls_object = new_cls_loader.loadClass("org.apache.commons.io.IOUtils")
        self.assertIsNotNone(cls_object)
        io_utils = reflect_class(cls_object)
        self.assertIsNotNone(io_utils)

        stringreader = autoclass("java.io.StringReader")("test1\ntest2")
        #lineIterator returns an object of class LineIterator - here we check that jnius can reflect that, despite not being in the boot classpath
        lineiter = io_utils.lineIterator(stringreader)
        self.assertEqual("test1", lineiter.next())
        self.assertEqual("test2", lineiter.next())

        # Equivalent Java code:  
        # var new_cls_loader = java.net.URLClassLoader.newInstance(new java.net.URL[] {new java.net.URL("https://repo1.maven.org/maven2/commons-io/commons-io/2.6/commons-io-2.6.jar")}, ClassLoader.getSystemClassLoader())
        # var cls = new_cls_loader.loadClass("org.apache.commons.io.IOUtils")
        # var sr = new java.io.StringReader("test1\ntest2")
        # var m = $2.getMethod("lineIterator", Reader.class)
        # m.invoke(null, (Object) sr)