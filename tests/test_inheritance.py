from jnius import autoclass


def test_methodcalls():
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert parent.doCall(parent) == 0
    assert child.doCall(0) == 1
    assert child.doCall(child) == 0

def test_fields():
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert parent.PARENT_FIELD == 0
    assert child.CHILD_FIELD == 1
    assert child.PARENT_FIELD == 0
    

def test_newinstance():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')

    child = Child.newInstance()
    assert isinstance(child, Child)
    assert isinstance(child, Parent)

if __name__ == "__main__":
    test_newinstance()