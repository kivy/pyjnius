from __future__ import print_function
import sys
import imp

from jnius.reflect import autoclass

# Replacing builtin import following https://github.com/chaosct/pipimport/blob/79120eea4aed66743b5dbab47ba18a2d49c19638/pipimport/__init__.py
# (except this idea is at least a little bit better than that :<)

# Using a normal import hook doesn't work because it only receives the
# first part of the path


class JavaImporter(object):
    def __init__(self):
        self.real_import = __import__

    def __call__(self, name, *args, **kwargs):
        if not name.startswith('jnius.java.'):
            return self.real_import(name, *args, **kwargs)

        print('name is', name[11:])

        return autoclass(name[11:])


def replace_import():
    import __builtin__
    import_replacement = JavaImporter()
    __builtin__.__import__ = import_replacement
