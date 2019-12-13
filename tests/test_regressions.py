from jnius import autoclass


def test_465():
    arraylist = autoclass("java.util.ArrayList")()
    arraylist.iterator()
    arraylist.stream()
