# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
from jnius.reflect import autoclass


class ImplementationTest(unittest.TestCase):

    def test_println(self):
        # System.out.println implies recursive lookup, and j_self assignation.
        # It was crashing during the implementation :/
        System = autoclass('java.lang.System')
        System.out.println('')

    def test_printf(self):
        System = autoclass('java.lang.System')
        System.out.printf('hi\n')
        System.out.printf('hi %s %s\n', 'jnius', 'other string')

    def test_unicode(self):
        System = autoclass('java.lang.System')
        System.out.printf(u'é')

        Stack = autoclass('java.util.Stack')
        stack = Stack()
        emoji = u'\U0001F602'
        stack.push(emoji)
        popped = stack.pop()
        if sys.version_info < (3, 0):
            popped = popped.decode('utf-8')
        self.assertEqual(emoji, popped)
