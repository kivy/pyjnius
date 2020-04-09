'''
Test creating for java.io.Closeable dunder
'''

from __future__ import absolute_import
import unittest
from jnius import autoclass, JavaException, protocol_map


class TestCloseable(unittest.TestCase):
    '''
    TestCase for using java.io.Closeable dunder
    '''

    def test_stringreader_closeable(self):
        '''
        this checkes that java.lang.AutoCloseable instances gain
        the correct dunder methods
        '''
        swCheck = autoclass("java.io.StringWriter")()
        self.assertTrue("__enter__" in dir(swCheck))
        self.assertTrue("__exit__" in dir(swCheck))

        with autoclass("java.io.StringWriter")() as sw:
            sw.write("Hello")
            
    def test_our_closeable(self):
        '''
        this checkes that closeable dunder methods are actually called
        org.jnius.CloseableClass has java.io.Closeable, to differ from
        java.lang.AutoCloseable (which is what is in interface_map)
        '''
        ourcloseableClz = autoclass("org.jnius.CloseableClass")
        self.assertTrue("__enter__" in dir(ourcloseableClz()))
        self.assertTrue("__exit__" in dir(ourcloseableClz()))

        self.assertTrue(ourcloseableClz.open)
        with ourcloseableClz() as ourcloseable2:
            self.assertTrue(ourcloseableClz.open)
        self.assertFalse(ourcloseableClz.open)

    def test_protocol_map(self):
       self.assertTrue("java.util.List" in protocol_map)
