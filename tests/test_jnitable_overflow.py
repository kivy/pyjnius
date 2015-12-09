from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# run it, and check with Java VisualVM if we are eating too much memory or not!
if __name__ == '__main__':
    from jnius import autoclass
    Stack = autoclass('java.util.Stack')
    i = 0
    while True:
        i += 1
        stack = Stack()
        stack.push('hello')
