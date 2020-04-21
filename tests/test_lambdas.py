import unittest

from jnius import autoclass, JavaException

class TestLambdas(unittest.TestCase):

    def testCallable(self):
        callFn = lambda: "done"
        executor = autoclass("java.util.concurrent.Executors").newFixedThreadPool(1)
        future = executor.submit(callFn)
        print(type(future))
        self.assertEqual("done", future.get())
        executor.shutdownNow()

    def testComparator(self):
        numbers = autoclass('java.util.ArrayList')()
        Collections = autoclass('java.util.Collections')
        numbers.add(1)
        numbers.add(3)
        revSort = lambda i, j: j - i 
        Collections.sort(numbers, revSort)
        self.assertEqual(numbers[0], 3)
        self.assertEqual(numbers[1], 1)

    def testJavaUtilFunction(self):
        Collectors = autoclass("java.util.stream.Collectors")
        numbers = autoclass('java.util.ArrayList')()
        numbers.add(1)
        numbers.add(2)
        numbers.add(3)

        def squareFn(i):
            return i * i

        
        #J: List<Integer> squares = numbers.stream().map( i -> i*i).collect(Collectors.toList());
        squares = numbers.stream().map(lambda i : i * i).collect(Collectors.toList())

        self.assertEqual(len(squares), len(numbers))
        self.assertEqual(squares[0], 1)
        self.assertEqual(squares[1], 4)
        self.assertEqual(squares[2], 9)

        squares = numbers.stream().map(squareFn).collect(Collectors.toList())

        self.assertEqual(len(squares), len(numbers))
        self.assertEqual(squares[0], 1)
        self.assertEqual(squares[1], 4)
        self.assertEqual(squares[2], 9)
        

if __name__ == '__main__':
    unittest.main()
