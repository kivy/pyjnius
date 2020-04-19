import unittest

from jnius import autoclass, JavaException

class TestLambdas(unittest.TestCase):

    def testJavaUtilFunction(self):
        Arrays = autoclass("java.util.Arrays")
        Collectors = autoclass("java.util.stream.Collectors")
        #J: List<Integer> numbers = Arrays.asList(1, 2, 3); 
        numbers = autoclass('java.util.ArrayList')()
        numbers.add(1)
        numbers.add(2)
        numbers.add(3)
        
        #J: List<Integer> squares = numbers.stream().map( i -> i*i).collect(Collectors.toList());
        squares = numbers.stream().map(lambda i : i * i).collect(Collectors.toList())

        self.assertEqual(len(squares), len(numbers))
        self.assertEqual(squares[0], 1)
        self.assertEqual(squares[1], 4)
        self.assertEqual(squares[2], 9)
        

if __name__ == '__main__':
    unittest.main()
