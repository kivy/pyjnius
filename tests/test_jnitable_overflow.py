# run it, and check with Java VisualVM if we are eating too much memory or not!
from jnius import autoclass

Stack = autoclass('java.util.Stack')
i = 0
while True:
    i += 1
    stack = Stack()
    stack.push('hello')
