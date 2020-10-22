from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius import autoclass

class PassByReferenceOrValueTest(unittest.TestCase):

    def _verify(self, numbers, changed):
        for i in range(len(numbers)):
            self.assertEqual(numbers[i], i * i if changed else i)

    def _verify_all(self, numbers, changed):
            for n, c in zip(numbers, changed):
                self._verify(n, c)

    def test_single_param_static(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')

        # passed by reference (default), numbers should change
        numbers = list(range(10))
        VariablePassing.singleParamStatic(numbers)
        self._verify(numbers, True)

        # passed by reference, numbers should change
        numbers = list(range(10))
        VariablePassing.singleParamStatic(numbers, pass_by_reference=True)
        self._verify(numbers, True)

        # passed by value, numbers should not change
        numbers = list(range(10))
        VariablePassing.singleParamStatic(numbers, pass_by_reference=False)
        self._verify(numbers, False)

    def test_single_param(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')
        variablePassing = VariablePassing()

        # passed by reference (default), numbers should change
        numbers = list(range(10))
        variablePassing.singleParam(numbers)
        self._verify(numbers, True)

        # passed by reference, numbers should change
        numbers = list(range(10))
        variablePassing.singleParam(numbers, pass_by_reference=True)
        self._verify(numbers, True)

        # passed by value, numbers should not change
        numbers = list(range(10))
        variablePassing.singleParam(numbers, pass_by_reference=False)
        self._verify(numbers, False)

    def test_multiple_params_static(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')

        # passed by reference (default), all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        VariablePassing.multipleParamsStatic(*numbers)
        self._verify_all(numbers, [True] * 4)

        # passed by reference, all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=True)
        self._verify_all(numbers, [True] * 4)

        # passed by value, no numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=False)
        self._verify_all(numbers, [False] * 4)

        # only the first set of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=[True, False])
        self._verify_all(numbers, [True, False, False, False])

        # only the first set of numbers should not change
        numbers = [list(range(10)) for _ in range(4)]
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=[False, True])
        self._verify_all(numbers, [False, True, True, True])

        # only the odd sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (True, False, True, False)
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)

        # only the even sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (False, True, False, True)
        VariablePassing.multipleParamsStatic(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)

    def test_multiple_params(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')
        variablePassing = VariablePassing()

        # passed by reference (default), all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing.multipleParams(*numbers)
        self._verify_all(numbers, [True] * 4)

        # passed by reference, all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing.multipleParams(*numbers, pass_by_reference=True)
        self._verify_all(numbers, [True] * 4)

        # passed by value, no numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing.multipleParams(*numbers, pass_by_reference=False)
        self._verify_all(numbers, [False] * 4)

        # only the first set of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing.multipleParams(*numbers, pass_by_reference=[True, False])
        self._verify_all(numbers, [True, False, False, False])

        # only the first set of numbers should not change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing.multipleParams(*numbers, pass_by_reference=[False, True])
        self._verify_all(numbers, [False, True, True, True])

        # only the odd sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (True, False, True, False)
        variablePassing.multipleParams(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)

        # only the even sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (False, True, False, True)
        variablePassing.multipleParams(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)

    def test_contructor_single_param(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')

        # passed by reference (default), numbers should change
        numbers = list(range(10))
        variablePassing = VariablePassing(numbers)
        self._verify(numbers, True)

        # passed by reference, numbers should change
        numbers = list(range(10))
        variablePassing = VariablePassing(numbers, pass_by_reference=True)
        self._verify(numbers, True)

        # passed by value, numbers should not change
        numbers = list(range(10))
        variablePassing = VariablePassing(numbers, pass_by_reference=False)
        self._verify(numbers, False)

    def test_contructor_multiple_params(self):
        VariablePassing = autoclass('org.jnius.VariablePassing')

        # passed by reference (default), all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing = VariablePassing(*numbers)
        self._verify_all(numbers, [True] * 4)

        # passed by reference, all numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing = VariablePassing(*numbers, pass_by_reference=True)
        self._verify_all(numbers, [True] * 4)

        # passed by value, no numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing = VariablePassing(*numbers, pass_by_reference=False)
        self._verify_all(numbers, [False] * 4)

        # only the first set of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing = VariablePassing(*numbers, pass_by_reference=[True, False])
        self._verify_all(numbers, [True, False, False, False])

        # only the first set of numbers should not change
        numbers = [list(range(10)) for _ in range(4)]
        variablePassing = VariablePassing(*numbers, pass_by_reference=[False, True])
        self._verify_all(numbers, [False, True, True, True])

        # only the odd sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (True, False, True, False)
        variablePassing = VariablePassing(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)

        # only the even sets of numbers should change
        numbers = [list(range(10)) for _ in range(4)]
        changed = (False, True, False, True)
        variablePassing = VariablePassing(*numbers, pass_by_reference=changed)
        self._verify_all(numbers, changed)
