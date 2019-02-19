from jnius import autoclass

def test_newinstance():
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')

    child = Child.newInstance()

    assert isinstance(child, Child)
    assert isinstance(child, Parent)
