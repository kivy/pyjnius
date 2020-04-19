

def test_methodcalls():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')
    child = Child.newInstance()
    parent = Parent.newInstance()
    assert parent.doCall(parent) == 0
    assert child.doCall(0) == 1
    assert child.doCall(child) == 0

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
    assert Parent.StaticGetParentStaticField() == 1
    assert Child.STATIC_PARENT_FIELD == 1
    assert Child.StaticGetParentStaticField() == 1
    assert parent.STATIC_PARENT_FIELD == 1
    assert child.STATIC_PARENT_FIELD == 1
    assert parent.StaticGetParentStaticField() == 1
    assert child.StaticGetParentStaticField() == 1
    assert parent.getParentStaticField() == 1
    assert child.getParentStaticField() == 1

    # now test setting in parent
    Parent.STATIC_PARENT_FIELD = 5
    assert parent.STATIC_PARENT_FIELD == 5
    assert Child.STATIC_PARENT_FIELD == 5
    assert child.STATIC_PARENT_FIELD == 5
    assert Parent.StaticGetParentStaticField() == 5
    assert Child.StaticGetParentStaticField() == 5
    assert parent.StaticGetParentStaticField() == 5
    assert child.StaticGetParentStaticField() == 5
    assert parent.getParentStaticField() == 5
    assert child.getParentStaticField() == 5
    
    # now test setting in child
    child.STATIC_PARENT_FIELD = 10
    assert Child.STATIC_PARENT_FIELD == 10
    assert child.STATIC_PARENT_FIELD == 10
    assert Parent.STATIC_PARENT_FIELD == 10
    assert parent.STATIC_PARENT_FIELD == 10
    assert Parent.StaticGetParentStaticField() == 10
    assert Child.StaticGetParentStaticField() == 10
    assert parent.StaticGetParentStaticField() == 10
    assert child.StaticGetParentStaticField() == 10
    assert parent.getParentStaticField() == 10
    assert child.getParentStaticField() == 10

def test_newinstance():
    from jnius import autoclass
    Parent = autoclass('org.jnius.Parent')
    Child = autoclass('org.jnius.Child')

    child = Child.newInstance()
    assert isinstance(child, Child)
    assert isinstance(child, Parent)

if __name__ == "__main__":
    import jnius_config
    #jnius_config.add_options('-Xcheck:jni')
    test_staticfields()

