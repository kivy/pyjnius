"""Saved Java methods keep their original receiver (issue #47)."""

import gc

import pytest

from jnius import autoclass, JavaException, JavaMethod, JavaMultipleMethod


@pytest.fixture
def fixture_class():
    return autoclass('org.jnius.MethodBindingTest')


@pytest.mark.parametrize('name', ['single', 'multiple'])
@pytest.mark.parametrize('through_instance', [False, True])
def test_python_class_attribute(fixture_class, name, through_instance):
    original = fixture_class('original')

    class Holder:
        method = getattr(original, name)

    holder = Holder() if through_instance else Holder
    assert holder.method() == 'original'
    if name == 'multiple':
        assert holder.method(':suffix') == 'original:suffix'


@pytest.mark.parametrize('name', ['single', 'multiple'])
def test_local_alias_and_python_instance_attribute(fixture_class, name):
    original = fixture_class('original')
    method = getattr(original, name)

    class Holder:
        pass

    holder = Holder()
    holder.method = method
    assert method() == 'original'
    assert holder.method() == 'original'
    if name == 'multiple':
        assert method(':local') == 'original:local'
        assert holder.method(':instance') == 'original:instance'


@pytest.mark.parametrize('name', ['single', 'multiple'])
def test_saved_receivers_are_independent(fixture_class, name):
    first = fixture_class('first')
    second = fixture_class('second')
    first_method = getattr(first, name)
    second_method = getattr(second, name)

    for _ in range(2):
        assert first_method() == 'first'
        assert second_method() == 'second'
        assert getattr(first, name)() == 'first'
        assert second_method() == 'second'
        assert getattr(second, name)() == 'second'
        assert first_method() == 'first'
        # A Java-class lookup must neither unbind nor redirect saved methods.
        getattr(fixture_class, name)
        assert first_method() == 'first'
        assert second_method() == 'second'
        if name == 'multiple':
            assert first_method(':x') == 'first:x'
            assert second_method(':y') == 'second:y'


@pytest.mark.parametrize('name, descriptor_type', [
    ('single', JavaMethod),
    ('multiple', JavaMultipleMethod),
])
def test_java_class_access_remains_unbound(fixture_class, name, descriptor_type):
    descriptor = fixture_class.__dict__[name]
    original = fixture_class('original')
    method = getattr(original, name)
    assert method() == 'original'
    class_method = getattr(fixture_class, name)
    assert class_method is descriptor
    assert isinstance(class_method, descriptor_type)
    with pytest.raises(JavaException):
        class_method()
    assert method() == 'original'


@pytest.mark.parametrize('name', ['single', 'multiple'])
def test_instance_descriptor_rejects_python_receiver(fixture_class, name):
    class Holder:
        method = getattr(fixture_class, name)

    assert Holder.method is getattr(fixture_class, name)
    with pytest.raises(TypeError):
        Holder().method


@pytest.mark.parametrize('name', ['staticSingle', 'staticMultiple'])
def test_static_methods_on_python_class(fixture_class, name):
    class Holder:
        method = getattr(fixture_class, name)

    for holder in (fixture_class, Holder, Holder()):
        method = getattr(holder, name) if holder is fixture_class else holder.method
        assert method() == 'static'
        if name == 'staticMultiple':
            assert method(':suffix') == 'static:suffix'


@pytest.mark.parametrize('name', ['single', 'multiple'])
def test_bound_signatures(fixture_class, name):
    original = fixture_class('original')
    method = getattr(original, name)
    assert method.signatures() == getattr(fixture_class, name).signatures()
    assert method() == 'original'


@pytest.mark.parametrize('name', ['single', 'multiple'])
def test_saved_callable_keeps_receiver_alive(fixture_class, name):
    def save_method():
        original = fixture_class('original')
        return getattr(original, name)

    method = save_method()
    gc.collect()
    # Replace any shared descriptor receiver before checking the saved one.
    other = fixture_class('other')
    assert getattr(other, name)() == 'other'
    gc.collect()
    assert method() == 'original'
    if name == 'multiple':
        assert method(':alive') == 'original:alive'


@pytest.mark.parametrize('through_instance', [False, True])
def test_system_out_class_attribute(through_instance):
    System = autoclass('java.lang.System')

    class Holder:
        println = System.out.println

    holder = Holder() if through_instance else Holder
    assert list(map(holder.println, ['issue #47'])) == [None]
