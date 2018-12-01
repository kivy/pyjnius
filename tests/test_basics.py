from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
from jnius.reflect import autoclass

try:
    long
except NameError:
    # Python 3
    long = int

def py2_encode(uni):
    if sys.version_info < (3, 0):
        uni = uni.encode('utf-8')
    return uni


class BasicsTest(unittest.TestCase):

    def test_static_methods(self):
        Test = autoclass('org.jnius.BasicsTest')
        self.assertEquals(Test.methodStaticZ(), True)
        self.assertEquals(Test.methodStaticB(), 127)
        self.assertEquals(Test.methodStaticC(), 'k')
        self.assertEquals(Test.methodStaticS(), 32767)
        self.assertEquals(Test.methodStaticI(), 2147483467)
        self.assertEquals(Test.methodStaticJ(), 9223372036854775807)
        self.assertAlmostEquals(Test.methodStaticF(), 1.23456789)
        self.assertEquals(Test.methodStaticD(), 1.23456789)
        self.assertEquals(Test.methodStaticString(), py2_encode(u'hello \U0001F30E!'))

    def test_static_fields(self):
        Test = autoclass('org.jnius.BasicsTest')
        self.assertEquals(Test.fieldStaticZ, True)
        self.assertEquals(Test.fieldStaticB, 127)
        self.assertEquals(Test.fieldStaticC, 'k')
        self.assertEquals(Test.fieldStaticS, 32767)
        self.assertEquals(Test.fieldStaticI, 2147483467)
        self.assertEquals(Test.fieldStaticJ, 9223372036854775807)
        self.assertAlmostEquals(Test.fieldStaticF, 1.23456789)
        self.assertEquals(Test.fieldStaticD, 1.23456789)
        self.assertEquals(Test.fieldStaticString, py2_encode(u'hello \U0001F30E!'))

    def test_instance_methods(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodZ(), True)
        self.assertEquals(test.methodB(), 127)
        self.assertEquals(test.methodC(), 'k')
        self.assertEquals(test.methodS(), 32767)
        self.assertEquals(test.methodI(), 2147483467)
        self.assertEquals(test.methodJ(), 9223372036854775807)
        self.assertAlmostEquals(test.methodF(), 1.23456789)
        self.assertEquals(test.methodD(), 1.23456789)
        self.assertEquals(test.methodString(), py2_encode(u'hello \U0001F30E!'))

    def test_instance_fields(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.fieldZ, True)
        self.assertEquals(test.fieldB, 127)
        self.assertEquals(test.fieldC, 'k')
        self.assertEquals(test.fieldS, 32767)
        self.assertEquals(test.fieldI, 2147483467)
        self.assertEquals(test.fieldJ, 9223372036854775807)
        self.assertAlmostEquals(test.fieldF, 1.23456789)
        self.assertEquals(test.fieldD, 1.23456789)
        self.assertEquals(test.fieldString, py2_encode(u'hello \U0001F30E!'))
        test2 = autoclass('org.jnius.BasicsTest')(10)
        self.assertEquals(test2.fieldB, 10)
        self.assertEquals(test.fieldB, 127)
        self.assertEquals(test2.fieldB, 10)

    def test_instance_getter_naming(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.disabled, True)
        self.assertEquals(test.enabled, False)

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
        self.assertEquals(test.methodArrayZ(), [True] * 3)
        self.assertEquals(test.methodArrayB()[0], 127)
        if sys.version_info >= (3, 0):
            self.assertEquals(test.methodArrayB(), [127] * 3)
        self.assertEquals(test.methodArrayC(), ['k'] * 3)
        self.assertEquals(test.methodArrayS(), [32767] * 3)
        self.assertEquals(test.methodArrayI(), [2147483467] * 3)
        self.assertEquals(test.methodArrayJ(), [9223372036854775807] * 3)

        ret = test.methodArrayF()
        ref = [1.23456789] * 3
        self.assertAlmostEquals(ret[0], ref[0])
        self.assertAlmostEquals(ret[1], ref[1])
        self.assertAlmostEquals(ret[2], ref[2])

        self.assertEquals(test.methodArrayD(), [1.23456789] * 3)
        self.assertEquals(test.methodArrayString(), [py2_encode(u'hello \U0001F30E!')] * 3)

    def test_instances_methods_params(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsZBCSIJFD(
            True, 127, 'k', 32767, 2147483467, 9223372036854775807, 1.23456789, 1.23456789), True)
        self.assertEquals(test.methodParamsZBCSIJFD(
            True, long(127), 'k', long(32767), long(2147483467), 9223372036854775807, 1.23456789, 1.23456789), True)
        self.assertEquals(test.methodParamsString(py2_encode(u'hello \U0001F30E!')), True)
        self.assertEquals(test.methodParamsArrayI([1, 2, 3]), True)
        self.assertEquals(test.methodParamsArrayString([
            py2_encode(u'hello'), py2_encode(u'\U0001F30E')]), True)

    def test_instances_methods_params_object_list_str(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsObject([
            'hello', 'world']), True)

    def test_instances_methods_params_object_list_int(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsObject([1, 2]), True)

    def test_instances_methods_params_object_list_float(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsObject([3.14, 1.61]), True)

    def test_instances_methods_params_object_list_long(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsObject([1, 2]), True)

    def test_instances_methods_params_array_byte(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodParamsArrayByte([127, 127, 127]), True)
        ret = test.methodArrayB()
        self.assertEquals(test.methodParamsArrayByte(ret), True)

    def test_return_array_as_object_array_of_strings(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodReturnStrings(), [py2_encode(u'Hello'),
                py2_encode(u'\U0001F30E')])

    def test_return_array_as_object_of_integers(self):
        test = autoclass('org.jnius.BasicsTest')()
        self.assertEquals(test.methodReturnIntegers(), [1, 2])
