from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest

from jnius import autoclass, JavaException


class Interface(unittest.TestCase):

    def test_reflect_interface(self):
        Interface = autoclass('org.jnius.InterfaceWithPublicEnum')
        self.assertTrue(Interface)

    def test_reflect_enum_in_interface(self):
        ATTITUDE = autoclass('org.jnius.InterfaceWithPublicEnum$ATTITUDE')
        self.assertTrue(ATTITUDE)
        self.assertTrue(ATTITUDE.GOOD)
        self.assertTrue(ATTITUDE.BAD)
        self.assertTrue(ATTITUDE.UGLY)
