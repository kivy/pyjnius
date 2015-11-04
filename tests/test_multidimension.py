from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass

class MultipleDimensionsTest(unittest.TestCase):

    def test_multiple_dimensions(self):
        MultipleDims = autoclass('org.jnius.MultipleDimensions')
        matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
        self.assertEquals(MultipleDims.methodParamsMatrixI(matrix), True)
        self.assertEquals(MultipleDims.methodReturnMatrixI(), matrix)
