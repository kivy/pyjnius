import unittest
from jnius.reflect import autoclass

class MultipleDimensionsTest(unittest.TestCase):

    def test_multiple_dimensions(self):
        MultipleDims = autoclass('org.jnius.MultipleDimensions')
        matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
        self.assertEqual(MultipleDims.methodParamsMatrixI(matrix), True)
        self.assertEqual(MultipleDims.methodReturnMatrixI(), matrix)
