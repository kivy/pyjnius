

from __future__ import absolute_import
import unittest
from jnius import autoclass, JavaException


class TestExceptions(unittest.TestCase):

    def test_exception(self):
        try:
            # expected to raise NPE, as per online javadoc
            autoclass("java.util.HashMap")(None)
            self.assertTrue(False)
        except JavaException as je:
            self.assertTrue(True)
            import traceback
            traceback.print_tb()
            #traceback.print_tb(je)
            #print(je)

         