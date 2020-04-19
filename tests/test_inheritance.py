import pytest


def test_methodcalls():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert parent.doCall(parent) == 0
    assert child.doCall(0) == 1
    assert child.doCall(child) == 0

@pytest.mark.skip
def test_name_clash_fields():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    print(dir(child))
    print(dir(parent))
    assert parent.CLASH_FIELD == 0
    assert child.CLASH_FIELD == 1
    assert child.super_CLASH_FIELD == 0


def test_fields():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert parent.PARENT_FIELD == 0
    assert child.CHILD_FIELD == 1
    assert child.PARENT_FIELD == 0

def test_staticfields():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert Parent.STATIC_PARENT_FIELD == 1
    assert Child.STATIC_PARENT_FIELD == 1
    assert parent.STATIC_PARENT_FIELD == 1
    assert child.STATIC_PARENT_FIELD == 1

    #now test setting
    Parent.STATIC_PARENT_FIELD = 5
    assert parent.STATIC_PARENT_FIELD == 5
    assert Parent.STATIC_PARENT_FIELD == 5
    assert Child.STATIC_PARENT_FIELD == 5
    assert child.STATIC_PARENT_FIELD == 5

    child.STATIC_PARENT_FIELD = 10
    assert Child.STATIC_PARENT_FIELD == 10
    assert child.STATIC_PARENT_FIELD == 10
    assert Parent.STATIC_PARENT_FIELD == 10
    assert parent.STATIC_PARENT_FIELD == 10

def test_newinstance():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')

    child = Child.newInstance()
    assert isinstance(child, Child)
    assert isinstance(child, Parent)

if __name__ == "__main__":
    import jnius_config
    jnius_config.add_options('-Xcheck:jni')
    test_newinstance()

