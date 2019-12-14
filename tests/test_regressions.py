from jnius import autoclass, cast


def test_465():
    arraylist = autoclass("java.util.ArrayList")()
    arraylist.iterator()
    cast('java.util.Collection', arraylist).stream()
    arraylist.stream()
