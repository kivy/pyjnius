from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import unittest
from jnius.reflect import autoclass


class BasicsTest(unittest.TestCase):

    def test_static_methods(self):
        Test = autoclass('org.jnius.BasicsTest')
        self.assertEqual(Test.methodStaticZ(), True)
        self.assertEqual(Test.methodStaticB(), 127)
        self.assertEqual(Test.methodStaticC(), 'k')
        self.assertEqual(Test.methodStaticS(), 32767)
        self.assertEqual(Test.methodStaticI(), 2147483467)
        self.assertEqual(Test.methodStaticJ(), 9223372036854775807)
        self.assertAlmostEqual(Test.methodStaticF(), 1.23456789)
        self.assertEqual(Test.methodStaticD(), 1.23456789)
        self.assertEqual(Test.methodStaticString(), 'hello \U0001F30E!')

    def test_static_fields(self):
        Test = autoclass('org.jnius.BasicsTest')
        self.assertEqual(Test.fieldStaticZ, True)
        self.assertEqual(Test.fieldStaticB, 127)
        self.assertEqual(Test.fieldStaticC, 'k')
        self.assertEqual(Test.fieldStaticS, 32767)
        self.assertEqual(Test.fieldStaticI, 2147483467)
        self.assertEqual(Test.fieldStaticJ, 9223372036854775807)
        self.assertAlmostEqual(Test.fieldStaticF, 1.23456789)
        self.assertEqual(Test.fieldStaticD, 1.23456789)
        self.assertEqual(Test.fieldStaticString, 'hello \U0001F30E!')

    def test_instance_methods(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodZ(), True)
        self.assertEqual(test.methodB(), 127)
        self.assertEqual(test.methodC(), 'k')
        self.assertEqual(test.methodS(), 32767)
        self.assertEqual(test.methodI(), 2147483467)
        self.assertEqual(test.methodJ(), 9223372036854775807)
        self.assertAlmostEqual(test.methodF(), 1.23456789)
        self.assertEqual(test.methodD(), 1.23456789)
        self.assertEqual(test.methodString(), 'hello \U0001F30E!')

    def test_instance_fields(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.fieldZ, True)
        self.assertEqual(test.fieldB, 127)
        self.assertEqual(test.fieldC, 'k')
        self.assertEqual(test.fieldS, 32767)
        self.assertEqual(test.fieldI, 2147483467)
        self.assertEqual(test.fieldJ, 9223372036854775807)
        self.assertAlmostEqual(test.fieldF, 1.23456789)
        self.assertEqual(test.fieldD, 1.23456789)
        self.assertEqual(test.fieldString, 'hello \U0001F30E!')
        test2 = autoclass('org.jnius.BasicsTest')(10)
        self.assertEqual(test2.fieldB, 10)
        self.assertEqual(test.fieldB, 127)
        self.assertEqual(test2.fieldB, 10)

    def test_instance_getter_naming(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.disabled, True)
        self.assertEqual(test.enabled, False)

    def test_instance_set_fields(self):
        test = autoclass('org.jnius.BasicsTest')()
        test.fieldSetZ = True
        test.fieldSetB = 127
        test.fieldSetC = ord('k')
        test.fieldSetS = 32767
        test.fieldSetI = 2147483467
        test.fieldSetJ = 9223372036854775807
        test.fieldSetF = 1.23456789
        test.fieldSetD = 1.23456789

        self.assertTrue(test.testFieldSetZ())
        self.assertTrue(test.testFieldSetB())
        self.assertTrue(test.testFieldSetC())
        self.assertTrue(test.testFieldSetS())
        self.assertTrue(test.testFieldSetI())
        self.assertTrue(test.testFieldSetJ())
        self.assertTrue(test.testFieldSetF())
        self.assertTrue(test.testFieldSetD())

    def test_instances_methods_array(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodArrayZ(), [True] * 3)
        self.assertEqual(test.methodArrayB()[0], 127)
        self.assertEqual(test.methodArrayB(), [127] * 3)
        self.assertEqual(test.methodArrayC(), ['k'] * 3)
        self.assertEqual(test.methodArrayS(), [32767] * 3)
        self.assertEqual(test.methodArrayI(), [2147483467] * 3)
        self.assertEqual(test.methodArrayJ(), [9223372036854775807] * 3)

        ret = test.methodArrayF()
        ref = [1.23456789] * 3
        self.assertAlmostEqual(ret[0], ref[0])
        self.assertAlmostEqual(ret[1], ref[1])
        self.assertAlmostEqual(ret[2], ref[2])

        self.assertEqual(test.methodArrayD(), [1.23456789] * 3)
        self.assertEqual(test.methodArrayString(), ['hello \U0001F30E!'] * 3)

    def test_instances_methods_params(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodParamsZBCSIJFD(
            True, 127, 'k', 32767, 2147483467, 9223372036854775807, 1.23456789, 1.23456789), True)
        self.assertEqual(test.methodParamsString('hello \U0001F30E!'), True)
        self.assertEqual(test.methodParamsArrayI([1, 2, 3]), True)
        self.assertEqual(test.methodParamsArrayString([
            'hello', '\U0001F30E']), True)

    def test_instances_methods_params_object_list_str(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodParamsObject([
            'hello', 'world']), True)

    def test_instances_methods_params_object_list_int(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodParamsObject([1, 2]), True)

    def test_instances_methods_params_object_list_float(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodParamsObject([3.14, 1.61]), True)

    def test_instances_methods_params_array_byte(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodParamsArrayByte([127, 127, 127]), True)
        ret = test.methodArrayB()
        self.assertEqual(test.methodParamsArrayByte(ret), True)

    def test_return_array_as_object_array_of_strings(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodReturnStrings(), ['Hello',
                '\U0001F30E'])

    def test_return_array_as_object_of_integers(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEqual(test.methodReturnIntegers(), [1, 2])
