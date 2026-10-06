from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import os
import pytest
import subprocess
import sys
import textwrap
import unittest
from jnius.reflect import autoclass
from jnius import cast, JavaException
from jnius.reflect import identify_hierarchy
from jnius import find_javaclass

def identify_hierarchy_dict(cls, level, concrete=True):
    return({ cls.getName() : level for cls,level in identify_hierarchy(cls, level, concrete) })

class ReflectTest(unittest.TestCase):

    def assertContains(self, d, clsName):
        self.assertTrue(clsName in d, clsName + " was not found in " + str(d))

    def test_hierharchy_queue(self):
        d = identify_hierarchy_dict(find_javaclass("java.util.Queue"), 0, False)
        self.assertContains(d, "java.util.Queue")
        # super interfaces
        self.assertContains(d, "java.util.Collection")
        self.assertContains(d, "java.lang.Iterable")
        # all instantiated interfaces are rooted at Object
        self.assertContains(d, "java.lang.Object")
        maxLevel = max(d.values())
        self.assertEqual(d["java.lang.Object"], maxLevel)
        self.assertEqual(d["java.util.Queue"], 0)
        
    def test_hierharchy_arraylist(self):
        d = identify_hierarchy_dict(find_javaclass("java.util.ArrayList"), 0, True)
        self.assertContains(d, "java.util.ArrayList")# concrete
        self.assertContains(d, "java.util.AbstractCollection")# superclass
        self.assertContains(d, "java.util.Collection")# interface
        self.assertContains(d, "java.lang.Iterable")# interface
        self.assertContains(d, "java.lang.Object")# root
        maxLevel = max(d.values())
        self.assertTrue(d["java.lang.Object"] in [maxLevel, maxLevel -1]) # Object should be pretty high up the hierarchy. 
        self.assertEqual(d["java.util.ArrayList"], 0)

    def test_class(self):
        lstClz = autoclass("java.util.List")
        self.assertTrue("_class" in dir(lstClz))
        self.assertEqual("java.util.List", lstClz._class.getName())
        alstClz = autoclass("java.util.ArrayList")
        self.assertTrue("_class" in dir(alstClz))
        self.assertEqual("java.util.ArrayList", alstClz._class.getName())
        self.assertEqual("java.util.ArrayList", alstClz().getClass().getName())

    def test_stack(self):
        Stack = autoclass('java.util.Stack')
        stack = Stack()
        self.assertIsInstance(stack, Stack)
        stack.push('hello')
        stack.push('world')
        self.assertEqual(stack.pop(), 'world')
        self.assertEqual(stack.pop(), 'hello')
    
    def test_collection(self):
        HashSet = autoclass('java.util.HashSet')
        aset = HashSet()
        aset.add('hello')
        aset.add('world')
        #check that the __len__ dunder is applied to a Collection not a List
        self.assertEqual(2, len(aset))
        #check that the __len__ dunder is applied to it cast as a Collection
        self.assertEqual(2, len(cast("java.util.Collection", aset)))

    def test_list_interface(self):
        ArrayList = autoclass('java.util.ArrayList')
        words = ArrayList()
        words.add('hello')
        words.add('world')
        self.assertIsNotNone(words.stream())
        self.assertIsNotNone(words.iterator())

    def test_super_interface(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        words.add('hello')
        words.add('world')
        q = cast('java.util.Queue', words)
        self.assertEqual(2, q.size())
        self.assertEqual(2, len(q))
        self.assertIsNotNone(q.iterator())

    def test_super_object(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        words.hashCode()

    def test_super_interface_object(self):
        LinkedList = autoclass('java.util.LinkedList')
        words = LinkedList()
        q = cast('java.util.Queue', words)
        q.hashCode()

    def test_list_iteration(self):
        ArrayList = autoclass('java.util.ArrayList')
        words = ArrayList()
        words.add('hello')
        words.add('world')
        self.assertEqual(['hello', 'world'], [word for word in words])

    @pytest.mark.skipif(
        sys.platform == 'android' or 'ANDROID_ARGUMENT' in os.environ,
        reason='Android does not bundle the desktop Logger helper'
    )
    def test_named_logger_from_python(self):
        Logger = autoclass('java.util.logging.Logger')
        logger = Logger.getLogger('org.jnius.issue623')
        self.assertEqual('org.jnius.issue623', logger.getName())
        self.assertEqual(logger.hashCode(), Logger.getLogger('org.jnius.issue623').hashCode())

        # The two-String overload still reports ordinary Java bundle errors,
        # rather than failing because the JNI caller has no Java frame.
        with self.assertRaises(JavaException) as caught:
            Logger.getLogger('org.jnius.issue623.bundle', 'org.jnius.missing.bundle')
        self.assertEqual('java.util.MissingResourceException', caught.exception.classname)

    @pytest.mark.skipif(
        sys.platform == 'android' or 'ANDROID_ARGUMENT' in os.environ,
        reason='Android does not bundle the desktop Logger helper'
    )
    def test_named_logger_without_helper_on_classpath(self):
        # Run in a fresh JVM without PyJNIus's bundled Java classes. A missing
        # helper must preserve the old direct JNI call, which can work on JDK 8.
        script = textwrap.dedent('''\
            import jnius_config
            jnius_config.expand_classpath = lambda: ''
            from jnius import autoclass, JavaException

            try:
                autoclass('org.jnius.LoggerHelper')
            except JavaException as exc:
                assert exc.classname == 'java.lang.NoClassDefFoundError', exc
            else:
                raise AssertionError('helper unexpectedly present')

            try:
                autoclass('java.util.logging.Logger').getLogger('org.jnius.issue623.fallback')
            except JavaException as exc:
                assert exc.classname == 'java.lang.NullPointerException', exc
            ''')
        process = subprocess.run(
            [sys.executable, '-c', script], capture_output=True, text=True
        )
        self.assertEqual(0, process.returncode, process.stderr)
