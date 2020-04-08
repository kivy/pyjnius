'''
Test creating for java.io.Closeable dunder
'''

from __future__ import absolute_import
import unittest
from jnius import autoclass, JavaException, interface_map


class TestConstructor(unittest.TestCase):
    '''
    TestCase for using java.io.Closeable dunder
    '''

    #this checkes that closeable are converted to the correct dunder methods
    def test_stringreader_closeable(self):
        swCheck = autoclass("java.io.StringWriter")()
        self.assertTrue("__enter__" in dir(swCheck))
        self.assertTrue("__exit__" in dir(swCheck))

        with autoclass("java.io.StringWriter")() as sw:
            sw.write("Hello")
            
    #this checkes that closeable dunder methods are actually called
    def test_our_closeable(self):
        ourcloseableClz = autoclass("org.jnius.CloseableClass")
        self.assertTrue("__enter__" in dir(ourcloseableClz()))
        self.assertTrue("__exit__" in dir(ourcloseableClz()))

        self.assertTrue(ourcloseableClz.open)
        with ourcloseableClz() as ourcloseable2:
            self.assertTrue(ourcloseableClz.open)
        self.assertFalse(ourcloseableClz.open)

    def test_interface_map(self):
       self.assertTrue("java.util.List" in interface_map)
